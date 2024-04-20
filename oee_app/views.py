from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import timedelta
from .models import Machines, ProductionLog
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.shortcuts import render,redirect

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Machines

@csrf_exempt
def add_machine(request):
    if request.method == 'POST':
        machine_name = request.POST.get('machine_name')
        machine_serial_no = request.POST.get('machine_serial_no')

        if not machine_name or not machine_serial_no:
            return render(request, 'main/add_machine.html', {
                'error': 'Missing required fields'
            })

        
        try:
            machine = Machines(
                machine_name=machine_name,
                machine_serial_no=machine_serial_no,
            )
            machine.save()

            
            return render(request, 'main/add_machine.html', {
                'success': 'Machine entry added successfully!'
            })

        except Exception as e:
            
            return render(request, 'main/add_machine.html', {
                'error': f'An error occurred: {str(e)}'
            })
    else:
        return render(request, 'main/add_machine.html')


@csrf_exempt
def add_production(request):
    if request.method == 'POST':
        try:
            data = request.POST
            cycle_no = data.get('cycle_no')
            unique_id = data.get('unique_id')
            material_name = data.get('material_name')
            machine_id = data.get('machine')
            start_time_str = data.get('start_time')
            end_time_str = data.get('end_time')
            duration = float(data.get('duration'))
            start_time = parse_datetime(start_time_str)
            end_time = parse_datetime(end_time_str)

            try:
                machine = Machines.objects.get(id=machine_id)
            except Machines.DoesNotExist:
                return JsonResponse({'error': 'Machine not found'}, status=400)

            production_log = ProductionLog(
                cycle_no=cycle_no,
                unique_id=unique_id,
                material_name=material_name,
                machine=machine,
                start_time=start_time,
                end_time=end_time,
                duration=duration
            )
            production_log.save()

            return redirect('add_production')

        except ValueError as e:
            
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            
            return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=400)
    
    else:
        
        return render(request, 'main/add_production.html')

def calculate_oee(machine):
    available_time_per_shift = 8  # Available time in hours per shift
    shifts_per_day = 3  # Number of shifts per day

    available_time = available_time_per_shift * shifts_per_day
    print(f"Available time: {available_time} hours")

   
    production_logs = ProductionLog.objects.filter(machine=machine)
    print(f"Production logs for machine {machine}: {production_logs}")

    
    total_good_products = 0
    total_bad_products = 0
    actual_output = 0
    available_operating_time = 0

    
    for log in production_logs:
        
        duration_in_minutes = log.duration * 60
        actual_output += duration_in_minutes
        
        
        if log.duration == 5:  # Assuming ideal cycle time is 5 minutes
            total_good_products += 1
        else:
            total_bad_products += 1
        
       
        available_operating_time += duration_in_minutes
    
    
    total_products_produced = total_good_products + total_bad_products
    if total_products_produced > 0:
        quality = (total_good_products / total_products_produced) * 100
    else:
        quality = 0
    
    print(f"Quality: {quality}%")

    
    ideal_cycle_time = 5  # Assuming ideal cycle time in minutes
    if available_operating_time > 0:
        ideal_output = total_good_products * ideal_cycle_time
        performance = (ideal_output / available_operating_time) * 100
    else:
        performance = 0
    
    print(f"Performance: {performance}%")

    
    if available_time > 0:
        unplanned_downtime = available_time - (available_operating_time / 60)
        availability = ((available_time - unplanned_downtime) / available_time) * 100
    else:
        availability = 0
    
    print(f"Availability: {availability}%")

    
    oee = (availability * performance * quality) / 100

    print(f"OEE for machine {machine}: {oee}%")

    return oee





@api_view(['GET'])
def get_oee(request):
    machines = Machines.objects.all()
    oee_data = {}

    for machine in machines:
        oee = calculate_oee(machine)
        oee_data[machine.machine_name] = oee
    
    return Response(oee_data)

