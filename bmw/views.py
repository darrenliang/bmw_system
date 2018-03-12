from datetime import datetime, timedelta
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
from .models import ChargerInfo, ChargerState, ChargerModel, ChargingRecord


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

        vchsocket = vchstate = intcurrentfeedback = intchargingcurrent = vchcommand = ""
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

def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect(reverse('rooms'))
            return redirect(reverse('log_in'))
        # else:
        #     logger.info("[log_in] errors={}".format(form.errors))

    return render(request, 'bmw/login.html', {'form': form})


def overview(request):
    return render(request, 'bmw/overview.html')


def devices(request):
    return render(request, 'bmw/devices.html')


def charts(request):
    return render(request, 'bmw/charts.html')


def details(request):
    return render(request, 'bmw/details.html')


def setting(request):
    return render(request, 'bmw/settings.html')


def audit_logs(request):
    return render(request, 'bmw/audit_logs.html')


def remote(request):
    return render(request, 'bmw/remote.html')


def test(request):
    return render(request, 'bmw/test.html')


def web_socket(request):
    return render(request, 'bmw/web_socket.html')


@login_required(login_url='/login/')
def logout(request):
    logout(request)
    return redirect(reverse('login'))


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


