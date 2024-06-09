from django.http import *
from django.shortcuts import render
from django.views import View
from .models import *
import datetime
import uuid
from django.db.models import Q

# Create your views here.
class ChooseLoginView(View):
    '''选择身份登录'''

    def get(self, request):
        return render(request, 'chooselogin.html')

class PatientLoginView(View):
    '''患者登录'''

    def get(self, request):
        return render(request, 'patientlogin.html')

    def post(self, request):
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')

        patient_list = Patient.objects.filter(phone=phone, password=password)
        if patient_list:
            request.session['patient'] = patient_list[0].phone
            return HttpResponseRedirect("/patientcenter/")

        return HttpResponse("登录有问题")

class DoctorLoginView(View):
    '''医生登录'''

    def get(self, request):
        return render(request, 'doctorlogin.html')

    def post(self, request):
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')

        doctor_list = Doctor.objects.filter(phone=phone, password=password)
        if doctor_list:
            request.session['doctor'] = doctor_list[0].phone
            return HttpResponseRedirect("/doctorcenter/")

        return HttpResponse("登录有问题")

class PatientRegisterView(View):
    '''患者注册'''

    def get(self, request):
        return render(request, 'patientregister.html')

    def post(self, request):
        # 只能注册患者账号 医生账号只能由管理员添加
        phone = request.POST.get('phone')

        patientlist = Patient.objects.filter(phone=phone)
        if patientlist:
            return render(request, 'patientregister.html', {"err": 1, "tips": "*该号码已经被注册"})
        else:
            password = request.POST.get('password', '')
            name = request.POST.get('name', '')
            sex = request.POST.get('sex', '')
            age = request.POST.get('age', '')

            patient = Patient.objects.create(phone=phone, password=password, name=name, sex=sex, age=age)

            if patient:
                return HttpResponseRedirect("/patientlogin/")

            return HttpResponseRedirect("/patientregister/")

class PatientCenterView(View):
    '''患者界面'''

    def get(self, request):
        patient_phone = request.session.get('patient')
        patientlist = Patient.objects.filter(phone=patient_phone)
        return render(request, 'patientcenter.html', {'patient_name': patientlist[0].name})

class ChooseDepartmentView(View):
    '''选择科室'''

    def get(self, request):
        parentid_department_list = [o.id for o in Department.objects.filter(parentid=0)]

        all_department_list = dict()
        for id in parentid_department_list:
            all_department_list[Department.objects.filter(id=id)[0].name] = Department.objects.filter(parentid=id)

        print(all_department_list)

        return render(request, 'choosedepartment.html', {'all_department_list': all_department_list})

class ChooseDoctorAndTimeView(View):
    '''选择医生和时间'''

    def get(self, request, department_id):
        department_id = int(department_id)

        department_name = Department.objects.get(id=department_id).name  # 科室名字

        doctor_list = Doctor.objects.filter(department_id=department_id)  # 当前科室里的医生

        doctor_time_number_list = []  # 此医生及其的可预约时间和人数列表
        for doctor in doctor_list:
            doctor_id = doctor.id
            doctor_time_number_list.append([doctor, TimeNumber.objects.get(doctor_id=doctor_id)])

        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        return render(request, 'choosedoctorandtime.html',
                      {'department_name': department_name, 'doctor_time_number_list': doctor_time_number_list,
                               'department_id': department_id, 'tomorrow': tomorrow})

class ConfirmRegistrationView(View):
    '''确认挂号信息'''

    def get(self, request, department_id, doctor_id, consultation_hours):
        department_id = int(department_id)
        doctor_id = int(doctor_id)

        patient_phone = request.session.get('patient')
        patient_list = Patient.objects.filter(phone=patient_phone)
        patient = patient_list[0]

        doctor = Doctor.objects.get(id=doctor_id)
        department = Department.objects.get(id=department_id)

        patient_name = patient.name
        doctor_name = doctor.name
        registration_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        consultation_hours = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
            "%Y-%m-%d") + " " + consultation_hours

        patient_id = patient.id
        address = department.address
        registration_price = doctor.registration_price
        # print(patient_name,doctor_name,registration_time,consultation_hours,doctor_id,patient_id,address)

        return render(request, 'confirmregistration.html', {'patient_name': patient_name,
                                                            'doctor_name': doctor_name,
                                                            'registration_time': registration_time,
                                                            'consultation_hours': consultation_hours,
                                                            'doctor_id': doctor_id,
                                                            'patient_id': patient_id,
                                                            'address': address,
                                                            'registration_price': registration_price})

    def post(self, request):
        patient_name = request.POST.get('patient_name', '')
        doctor_name = request.POST.get('doctor_name', '')
        registration_time = request.POST.get('registration_time', '')
        consultation_hours = request.POST.get('consultation_hours', '')
        illness = request.POST.get('illness', '')
        doctor_id = request.POST.get('doctor_id', '')
        patient_id = request.POST.get('patient_id', '')
        address = request.POST.get('address', '')
        out_trade_num = uuid.uuid4().hex
        payway = 'alipay'
        status = '待检查'
        isdelete = 0

        register = Register.objects.create(patient_name=patient_name, doctor_name=doctor_name,
                                           registration_time=registration_time,
                                           consultation_hours=consultation_hours, illness=illness, doctor_id=doctor_id,
                                           patient_id=patient_id, address=address, isdelete=isdelete,
                                           out_trade_num=out_trade_num,
                                           payway=payway, status=status)

        doctor_time_number = TimeNumber.objects.get(doctor_id=register.doctor_id)
        consultation_hours_time = str(register.consultation_hours)[11:]
        if consultation_hours_time == '08:00:00':
            doctor_time_number.eight -= 1
        elif consultation_hours_time == '09:00:00':
            doctor_time_number.nine -= 1
        elif consultation_hours_time == '10:00:00':
            doctor_time_number.ten -= 1
        elif consultation_hours_time == '11:00:00':
            doctor_time_number.eleven -= 1
        elif consultation_hours_time == '14:00:00':
            doctor_time_number.fourteen -= 1
        elif consultation_hours_time == '15:00:00':
            doctor_time_number.fifteen -= 1
        elif consultation_hours_time == '16:00:00':
            doctor_time_number.sixteen -= 1
        elif consultation_hours_time == '17:00:00':
            doctor_time_number.seventeen -= 1
        doctor_time_number.save()

        return HttpResponseRedirect('/patientshowregistration/')

class PatientShowRegistrationView(View):
    '''患者展示挂号信息'''

    def get(self, request):
        patient_phone = request.session.get('patient')
        patient_list = Patient.objects.filter(phone=patient_phone)
        patient = patient_list[0]
        register_list = patient.register_set.order_by('consultation_hours').filter(
            Q(isdelete=False, status='待检查') | Q(isdelete=False, status='已检查')).all()

        return render(request, 'patientshowregistration.html', {'register_list': register_list})


class GuideView(View):
    def get(self, request):
        return render(request, 'guide.html')


class TrafficView(View):
    def get(self, request):
        return render(request, 'traffic.html')


class DoctorCenterView(View):
    '''医生界面'''

    def get(self, request):
        doctor_phone = request.session.get('doctor', '')
        doctor_list = Doctor.objects.filter(phone=doctor_phone)
        doctor = doctor_list[0]
        return render(request, 'doctorcenter.html', {'doctor_name': doctor.name})


class DoctorShowRegistrationView(View):
    '''医生展示挂号信息'''

    def get(self, request):
        doctor_phone = request.session.get('doctor', '')
        doctor_list = Doctor.objects.filter(phone=doctor_phone)
        doctor = doctor_list[0]
        try:
            register_list = doctor.register_set.order_by('consultation_hours').filter(isdelete=0, status='待检查').all()
        except:
            register_list = []

        return render(request, 'doctorshowregistration.html', {'register_list': register_list})

    def post(self, request):
        register_id = request.POST.get('register_id', '')
        register = Register.objects.get(id=register_id)
        register.status = '已检查'
        register.save()

        doctor_phone = request.session.get('doctor', '')
        doctor_list = Doctor.objects.filter(phone=doctor_phone)
        doctor = doctor_list[0]
        try:
            register_list = doctor.register_set.order_by('consultation_hours').filter(isdelete=0, status='待检查').all()
        except:
            register_list = []

        return render(request, 'doctorshowregistration.html', {'register_list': register_list})