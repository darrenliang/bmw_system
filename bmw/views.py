from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status, authentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .models import ChargerInfo, ChargerState, ChargerModel, ChargingRecord, ChargerInfo, ChargerState, BasicSetting


@api_view(['GET'])
def get_user_info(request):
    user = request.user
    data = {"username": user.username if user else None}
    return Response(data)


@api_view(['GET'])
def get_charger_list(request):
    """
    相位仪表图，表示该点位电源供给方三个相位的电流使用情况。监控防止超出用量跳闸。
    右上角图标可进入设置界面设置该点位三个相位电流上限。
    上限电流作为负载均衡系统的分配参数供计算每台电桩充电时的最大电流。
    """

    if request.method == 'GET':
        data = []
        charger_info_list = ChargerInfo.objects.all()
        charger_state_list = ChargerState.objects.all()
        for charger_id in charger_info_list.values_list("vchchargerid", flat=True).union(
                charger_state_list.values_list("vchchargerid", flat=True)):
            charger_info = charger_info_list.filter(vchchargerid=charger_id).first()
            if charger_info is None:
                continue
            try:
                charger_state = charger_state_list.get(vchchargerid=charger_id)
                vch_state = charger_state.vchstate
            except ObjectDoesNotExist:
                vch_state = None
            data.append({"vch_charger_id": charger_id,
                         "vch_firmware_ver": charger_info.vchfirmwarever,
                         "vch_model_id": charger_info.vchmodelid,
                         "vch_state": vch_state})
        return Response({"data": data}, status=status.HTTP_200_OK)
    return Response({"message": "Error request method or None object!"},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_charger_id_list(request):
    """
    Charger id list的信息，用在充电电流图表变化根据charger_id查询
    """

    if request.method == 'GET':
        chargers = []
        charger_info_list = ChargerInfo.objects.all()
        for charger in charger_info_list:
            chargers.append(charger.vchchargerid)

        return Response({"chargers": chargers}, status=status.HTTP_200_OK)
    return Response({"message": "Error request method or None object!"},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_monthly_energy(request, charger_id=None):
    """
    SELECT sum(dblenergy) FROM evproject.charging_record where dttFinishTime
    between '2009-01-01' and '2009-02-01' and vchChargerID = ‘xxxxxxxx’;
    用如上示例SQL查询计算出前6个月每台电桩的充电量
    """

    if request.method == 'GET':
        charger_id = request.GET.get("charger_id") if charger_id is None else charger_id
        x = []
        y = []
        now = datetime.now()
        year = now.year
        month = now.month
        # year = 2015
        # month = 12

        queryset = ChargingRecord.objects.all()
        queryset = queryset if charger_id is None else queryset.filter(vchchargerid=charger_id)
        recent_months = 6 if charger_id is None else 12  # 排列1显示最近6个月，排列2显示最近12个月

        if queryset.count() < 1:
            return Response({"x": reversed(x), "y": reversed(y)}, status=status.HTTP_200_OK)
            # return Response({"message": "Cannot find the charger id={}!".format(charger_id)},
            #                 status=status.HTTP_400_BAD_REQUEST)

        for i in range(1, recent_months + 1):  # provide recent 6 month
            start_date = datetime(year=year, month=month, day=1)
            end_date = datetime(year=year if month < 12 else year + 1, month=month + 1 if month < 12 else 1, day=1)
            month_queryset = queryset.filter(dttfinishtime__gte=start_date, dttfinishtime__lt=end_date)
            sum_energy = sum([charger.dblenergy for charger in month_queryset])

            dt = datetime.strptime("{}-{}".format(year, month), "%Y-%m")
            x.append(dt.strftime("%Y-%m"))
            y.append(sum_energy)

            month = month - 1 if month > 1 else 12
            year = year - 1 if month == 12 else year

        return Response({"x": reversed(x), "y": reversed(y)}, status=status.HTTP_200_OK)
    return Response({"message": "Error request method or None object!"},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_monthly_energy_list(request):
    """
    SELECT sum(dblenergy) FROM evproject.charging_record where dttFinishTime
    between '2009-01-01' and '2009-02-01' and vchChargerID = ‘xxxxxxxx’;
    用如上示例SQL查询计算出前6个月每台电桩的充电量
    """

    if request.method == 'GET':
        data = []
        for charger_id in get_charger_id_list(request).data["chargers"]:
            x = list(get_monthly_energy(request, charger_id).data["x"])
            y = list(get_monthly_energy(request, charger_id).data["y"])
            if len(x) > 0 and len(y) > 0:
                data.append(dict(charger_id=charger_id, x=x, y=y))
        return Response({"data": data}, status=status.HTTP_200_OK)
    return Response({"message": "Error request method or None object!"},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_max_current_list(request):
    """
    点位电桩列表，包含该点位所有电桩的实时情况和操作界面
    """
    if request.method == 'GET':
        basic_setting = BasicSetting.objects.first()
        if basic_setting:
            int_max_current_a = basic_setting.intmaxcurrenta
            int_max_current_b = basic_setting.intmaxcurrentb
            int_max_current_c = basic_setting.intmaxcurrentc
            return Response({"int_max_current_a": int_max_current_a,
                             "int_max_current_b": int_max_current_b,
                             "int_max_current_c": int_max_current_c},
                            status=status.HTTP_200_OK)
    return Response({"message": "Error request method or None object!"}, status=status.HTTP_400_BAD_REQUEST)


class ChargerStateStatisticView(APIView):
    """
        This view automatically provide `list` function
        """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = ChargerState.objects.all()

    def get(self, request):
        result = []
        state_list = ["BootUp", "Available", "PreParing", "Charging", "StatusChanged", "StopCharging",
                      "RemoteCharging", "RemoteStopCharging", "SendMessage", "Updating", "Unavailable", "Reboot",
                      "Faulted", "SupsendedEV", "Finishing", "Other"]
        accumulate_rate = 0
        size = self.queryset.count()
        for state in state_list:
            if state != "Other":
                rate = round(self.queryset.filter(vchstate=state).count() / size * 100, 2)
                result.append({state: rate})
                accumulate_rate += rate
            else:
                result.append({state: 100-accumulate_rate})
        return Response({"result": result}, status=status.HTTP_200_OK)


class RecentChargingRecordListView(APIView):
    """
        This view automatically provide `list` function
        """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = ChargingRecord.objects.all()  # vchchargerid

    def get(self, request):
        num = request.GET.get("num")
        num = int(num) if num else 7
        queryset = self.queryset.order_by("-dttfinishtime")[:num]
        record_list = []
        for record in queryset:
            record_list.append({"intrecordid": record.intrecordid,
                                "dttfinishtime": str(record.dttfinishtime).replace("T", " "),
                                "dblenergy": record.dblenergy})
        return Response({"num": num, "result": record_list}, status=status.HTTP_200_OK)


class RecentChargerStateListView(APIView):
    """
        This view automatically provide `list` function
        """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = ChargerState.objects.all()  # vchchargerid

    def get(self, request):
        num = request.GET.get("num")
        num = int(num) if num else 7
        queryset = self.queryset.order_by("-dttlastconntime")[:num]
        state_list = []
        for state in queryset:
            state_list.append({"vchchargerid": state.vchchargerid,
                               "vchstate": state.vchstate,
                               "vchcommand": state.vchcommand,
                               "dttlastconntime": state.dttlastconntime})
        return Response({"num": num, "result": state_list}, status=status.HTTP_200_OK)


class ChargerInfoStatisticView(APIView):
    """
        This view automatically provide `list` function
        """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    info_queryset = ChargerInfo.objects.all()  # vchchargerid
    state_queryset = ChargerState.objects.all()  # vchchargerid

    def get(self, request):
        total_charger = 0
        for info in self.info_queryset.all():
            for state in self.state_queryset.all():
                if info.vchchargerid == state.vchchargerid:
                    total_charger += 1
                    break

        accumulate_power = 0
        accumulate_minutes = 0
        for info in self.info_queryset.all():
            accumulate_power += info.dblaccumlatedpower
            accumulate_minutes += info.dblaccumlatedminute

        total_charging = 0
        charging_states = ["Charging", "SuspendedEV", "Finishing", "PreCharging"]
        for state in self.state_queryset.all():
            if state.vchstate in charging_states:
                total_charging += 1

        return Response({"total_charger": total_charger, "accumulate_power": round(accumulate_power, 2),
                         "accumulate_minutes": round(accumulate_minutes, 2), "total_charging": total_charging},
                        status=status.HTTP_200_OK)


class BasicSettingsView(APIView):
    """
    This view automatically provide `list` function
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = BasicSetting.objects.all()

    def get(self, request):
        basic_setting = self.queryset.first()
        vchcardreadercom = yeainstallyear = intinstallmonth = blncurrentdistribution = vchpowermetercom = \
            vchpowersequence = intcurrency = dblchargingdeductionpower = intchargingdeductionminute = \
            intdeductionprioritypower = intdeductionpriorityminute = dblpowercoefficient = blninternaltesting = \
            intmaxcurrenta = intmaxcurrentb = intmaxcurrentc = ""
        if basic_setting:
            vchcardreadercom = basic_setting.vchcardreadercom
            yeainstallyear = basic_setting.yeainstallyear
            intinstallmonth = basic_setting.intinstallmonth
            blncurrentdistribution = basic_setting.blncurrentdistribution
            vchpowermetercom = basic_setting.vchpowermetercom
            vchpowersequence = basic_setting.vchpowersequence
            # intcurrency = basic_setting.intcurrency
            dblchargingdeductionpower = basic_setting.dblchargingdeductionpower
            intdeductionpriorityminute = basic_setting.intdeductionpriorityminute
            intchargingdeductionminute = basic_setting.intchargingdeductionminute
            intdeductionprioritypower = basic_setting.intdeductionprioritypower
            dblpowercoefficient = basic_setting.dblpowercoefficient
            blninternaltesting = basic_setting.blninternaltesting
            intmaxcurrenta = basic_setting.intmaxcurrenta
            intmaxcurrentb = basic_setting.intmaxcurrentb
            intmaxcurrentc = basic_setting.intmaxcurrentc
        return Response({"vchcardreadercom": vchcardreadercom, "yeainstallyear": yeainstallyear,
                         "intinstallmonth": intinstallmonth, "blncurrentdistribution": blncurrentdistribution,
                         "vchpowermetercom": vchpowermetercom, "vchpowersequence": vchpowersequence,
                         "dblchargingdeductionpower": dblchargingdeductionpower,
                         "intchargingdeductionminute": intchargingdeductionminute,
                         "intdeductionprioritypower": intdeductionprioritypower,
                         "intdeductionpriorityminute": intdeductionpriorityminute,
                         "dblpowercoefficient": dblpowercoefficient, "blninternaltesting": blninternaltesting,
                         "intmaxcurrenta": intmaxcurrenta, "intmaxcurrentb": intmaxcurrentb,
                         "intmaxcurrentc": intmaxcurrentc}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            vchcardreadercom = request.POST.get("vchcardreadercom")
            yeainstallyear = request.POST.get("yeainstallyear")
            intinstallmonth = int(request.POST.get("intinstallmonth"))
            blncurrentdistribution = int(request.POST.get("blncurrentdistribution"))
            vchpowermetercom = request.POST.get("vchpowermetercom")
            vchpowersequence = request.POST.get("vchpowersequence")
            intcurrency = int(request.POST.get("intcurrency"))
            dblchargingdeductionpower = float(request.POST.get("dblchargingdeductionpower"))
            intdeductionpriorityminute = int(request.POST.get("intdeductionpriorityminute"))
            intchargingdeductionminute = int(request.POST.get("intchargingdeductionminute"))
            intdeductionprioritypower = int(request.POST.get("intdeductionprioritypower"))
            dblpowercoefficient = float(request.POST.get("dblpowercoefficient"))
            blninternaltesting = int(request.POST.get("blninternaltesting"))
            intmaxcurrenta = int(request.POST.get("intmaxcurrenta"))
            intmaxcurrentb = int(request.POST.get("intmaxcurrentb"))
            intmaxcurrentc = int(request.POST.get("intmaxcurrentc"))
            basic_setting = self.queryset.first()
            basic_setting.vchcardreadercom = vchcardreadercom
            basic_setting.yeainstallyear = yeainstallyear
            basic_setting.intinstallmonth = intinstallmonth
            basic_setting.blncurrentdistribution = blncurrentdistribution
            basic_setting.vchpowermetercom = vchpowermetercom
            basic_setting.vchpowersequence = vchpowersequence
            basic_setting.intcurrency = intcurrency
            basic_setting.dblchargingdeductionpower = dblchargingdeductionpower
            basic_setting.intdeductionpriorityminute = intdeductionpriorityminute
            basic_setting.intchargingdeductionminute = intchargingdeductionminute
            basic_setting.intdeductionprioritypower = intdeductionprioritypower
            basic_setting.dblpowercoefficient = dblpowercoefficient
            basic_setting.blninternaltesting = blninternaltesting
            basic_setting.intmaxcurrenta = intmaxcurrenta
            basic_setting.intmaxcurrentb = intmaxcurrentb
            basic_setting.intmaxcurrentc = intmaxcurrentc
            basic_setting.save()
            return Response({"vchcardreadercom": vchcardreadercom, "yeainstallyear": yeainstallyear,
                             "intinstallmonth": intinstallmonth, "blncurrentdistribution": blncurrentdistribution,
                             "vchpowermetercom": vchpowermetercom, "vchpowersequence": vchpowersequence,
                             "intcurrency": intcurrency, "dblchargingdeductionpower": dblchargingdeductionpower,
                             "intchargingdeductionminute": intchargingdeductionminute,
                             "intdeductionprioritypower": intdeductionprioritypower,
                             "intdeductionpriorityminute": intdeductionpriorityminute,
                             "dblpowercoefficient": dblpowercoefficient, "blninternaltesting": blninternaltesting,
                             "intmaxcurrenta": intmaxcurrenta, "intmaxcurrentb": intmaxcurrentb,
                             "intmaxcurrentc": intmaxcurrentc}, status=status.HTTP_200_OK)
        except Exception:
            raise ValueError("The parameters type error!")


class ChargingRecordDetails(APIView):
    """
    This view automatically provide `list` function
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = ChargingRecord.objects.all()

    def get(self, request):
        date = request.GET.get("date")
        record_list = []
        try:
            # room_mode = request.GET.get("room_mode")
            date_format = "%Y-%m-%d"
            start_date = datetime.strptime(date, date_format)
            end_date = datetime.strptime(date, date_format) + timedelta(hours=23, minutes=59, seconds=59)
            for record in self.queryset.filter(dttrealfinish__gte=start_date, dttrealfinish__lte=end_date):
                record_list.append({"intrecordid": record.intrecordid, "intchargingcode": record.intchargingcode,
                                    "vchchargerid": record.vchchargerid, "dttstartqueue": record.dttstartqueue,
                                    "dttstarttime": record.dttstarttime, "dttfinishtime": record.dttfinishtime,
                                    "dttrealfinish": record.dttrealfinish})
        except Exception:
            pass
        return Response({'result': record_list}, status=status.HTTP_200_OK)


class ChargerDetails(APIView):
    """
    This view automatically provide `list` function
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    info_queryset = ChargerInfo.objects.all()
    state_queryset = ChargerState.objects.all()
    model_queryset = ChargerModel.objects.all()

    def get(self, request):
        charger_id = "10245006"
        vchchargerid = vchmodelid = vchvenderid = vchserialno = vchfirmwarever = dblaccumlatedpower = vchip = vchmac = ""
        charger_infos = self.info_queryset.filter(vchchargerid=charger_id)
        if charger_infos.count() > 0:
            charger_info = charger_infos.first()
            vchchargerid = charger_info.vchchargerid
            vchmodelid = charger_info.vchmodelid
            vchvenderid = charger_info.vchvenderid
            vchserialno = charger_info.vchserialno
            vchfirmwarever = charger_info.vchfirmwarever
            dblaccumlatedpower = charger_info.dblaccumlatedpower
            dblaccumlatedminute = charger_info.dblaccumlatedminute
            vchip = charger_info.vchip
            vchmac = charger_info.vchmac

        vchsocket = vchstate = intcurrentfeedback = intcurrent = intchargingcurrent = intconsumedenergy = intelapsedtime = intchargingphase = vchcommand = ""
        charger_states = self.state_queryset.filter(vchchargerid=charger_id)
        if charger_states.count() > 0:
            charger_state = charger_states.first()
            vchsocket = charger_state.vchsocket
            vchstate = charger_state.vchstate
            intcurrentfeedback = charger_state.intcurrentfeedback
            intcurrent = charger_state.intcurrent
            intchargingcurrent = charger_state.intchargingcurrent
            intconsumedenergy = charger_state.intconsumedenergy
            intelapsedtime = charger_state.intelapsedtime
            intchargingphase = charger_state.intchargingphase
            vchcommand = charger_state.vchcommand

        dblmaxcurrent = dblmincurrent = intmaxphase = ""
        charger_models = self.model_queryset.filter(vchmodelid=vchmodelid)
        if charger_models.count() > 0:
            charger_model = charger_models.first()
            dblmaxcurrent = charger_model.dblmaxcurrent
            dblmincurrent = charger_model.dblmincurrent
            intmaxphase = charger_model.intmaxphase
        result = {"vchchargerid": vchchargerid, "vchModelID": vchmodelid, "vchvenderid": vchvenderid,
                  "vchSerialNo": vchserialno, "vchFirmwareVer": vchfirmwarever, "dblAccumlatedPower": dblaccumlatedpower,
                  "dblAccumlatedMinute": dblaccumlatedminute, "vchIP": vchip, "vchMac": vchmac,
                  "vchSoket": vchsocket, "vchstate": vchstate, "intcurrentfeedback": intcurrentfeedback,
                  "intcurrent": intcurrent, "intchargingcurrent": intchargingcurrent,
                  "intconsumedenergy": intconsumedenergy, "intElapsedTime": intelapsedtime,
                  "intchargingphase": intchargingphase, "vchcommand": vchcommand, "dblmaxcurrent": dblmaxcurrent,
                  "dblmincurrent": dblmincurrent, "intMaxPhase": intmaxphase}

        return Response({'result': result}, status=status.HTTP_200_OK)


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            authenticate(username=user.username, password=user.password)
            print("test come here")
            if user.is_staff or user.is_superuser:
                return redirect(reverse('overview'))
            return redirect(reverse('log_in'))
        # else:
        #     logger.info("[log_in] errors={}".format(form.errors))

    return render(request, 'bmw/login.html', {'form': form})


@login_required(login_url='/log_in/')
def overview(request):
    user = request.user
    if user is not None:
        print("user=", user.username)
        return render(request, 'bmw/overview.html')
    return redirect(reverse('log_in'))


@login_required(login_url='/log_in/')
def devices(request):
    user = request.user
    if user is not None:
        return render(request, 'bmw/devices.html')
    return redirect(reverse('log_in'))


@login_required(login_url='/log_in/')
def charts(request):
    user = request.user
    if user is not None:
        return render(request, 'bmw/charts.html')
    return redirect(reverse('log_in'))


@login_required(login_url='/log_in/')
def details(request):
    user = request.user
    if user is not None:
        return render(request, 'bmw/details.html')
    return redirect(reverse('log_in'))


@login_required(login_url='/log_in/')
def setting(request):
    user = request.user
    if user is not None:
        return render(request, 'bmw/settings.html')
    return redirect(reverse('log_in'))


@login_required(login_url='/log_in/')
def audit_logs(request):
    user = request.user
    if user is not None:
        return render(request, 'bmw/audit_logs.html')
    return redirect(reverse('log_in'))


@login_required(login_url='/log_in/')
def remote(request):
    return render(request, 'bmw/remote.html')


def test(request):
    return render(request, 'bmw/test.html')


def web_socket(request):
    return render(request, 'bmw/web_socket.html')


@login_required(login_url='/log_in/')
def log_out(request):
    logout(request)
    return redirect(reverse('log_in'))


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('log_in'))
        # else:
        #     logger.info("[sign_up] errors={}".format(form.errors))
    return render(request, 'bmw/sign_up.html', {'form': form})


