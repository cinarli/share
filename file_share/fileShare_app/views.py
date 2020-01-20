from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import MyFile,Comment
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from .tasks import my_first_task
from datetime import datetime,timedelta
User = get_user_model()



@login_required()
def simple_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            
            new_form = form.save(commit=False)
            new_form.user = request.user
            
            new_form.save()
            new_form.can_see.add(request.user)
            
            now=datetime.utcnow()
            my_first_task.apply_async(kwargs={'FormId':new_form.id},eta=now + timedelta(days=7))
            

            return JsonResponse({'error': False, 'message': 'Uploaded Successfully','fileid':new_form.id})
        else:
           return JsonResponse({'error': True, 'errors': form.errors})
        
    form = FileUploadForm()
    
    return render(request, 'home.html', {'form': form})

class FileDetailView(LoginRequiredMixin, DetailView):
    login_url ='empty:home'
    def get(self, request, *args, **kwargs):
        try:
            obj = MyFile.objects.get(id=kwargs['id'])
            can_see=obj.can_see.all()
            if request.user not in can_see:
                return redirect('empty:home')
        except:
            return redirect('empty:home')

       
        
        file_name = obj.a_file.name.split('/')[-1]

        format_file = file_name.split('.')[1]
        thumbnail = ''
        archive_format = ['zip', 'rar', '7z','7zip']
        file_type = ''
        image_format=['jpeg', 'png', 'jpg', 'gif']
        video_format = ['mp4', 'wmv', 'avi', 'ts', 'mov']
        voice_format=['mp3','aac','wav']
        #pc info
        
        if format_file in archive_format:
            file_type='archive'
            thumbnail = 'https://c7.uihere.com/files/10/164/877/computer-icons-zip-iconfinder-photos-icon-archive.jpg'
        elif format_file in image_format:
            file_type = 'image'
            thumbnail=''
        elif format_file in voice_format:
            file_type = 'voice'
            thumbnail=''
        elif format_file in video_format:
            file_type='video'
            thumbnail = ''
        else:
            thumbnail='https://s3.amazonaws.com/iconbros/icons/icon_pngs/000/000/288/original/file-empty.png'
        comments = Comment.objects.filter(file_obj=kwargs['id']).order_by('date')
        context = {'file': obj,'thumbnail':thumbnail,'name':file_name,'type':file_type,'comments':comments}
        return render(request, 'file.html',context=context)

@login_required
def myFilesView(request):
    
    obj = MyFile.objects.filter(user = request.user)
    return render(request, 'myfiles.html', context={
        'files' : obj
    })

@login_required
def deleteFile(request, id):
    try:
        obj = MyFile.objects.get(id=id)
        if obj.user==request.user:
            obj.delete()
            return redirect('empty:home')
    except:
        return redirect('empty:home')

    return redirect('empty:home')


@login_required
def deleteComment(request):
    id = request.GET.get('id')
    try:
        obj = Comment.objects.get(id=id)
    except:
        return JsonResponse(data={'error': 'Comment tapılmadı'})
    if obj.User == request.user or request.user == obj.file_obj.user :
        try:
            obj.delete()
            return JsonResponse(data={'success': 'Comment silindi'})
        except:
            return JsonResponse(data={'error': 'Xəta baş verdi'})
    else:
        return JsonResponse(data={'error':'Bu kommenti silə bilməzsiniz'})

@login_required
def editComment(request):
    comId = request.GET.get('comId')
    message = request.GET.get('msg')
    try:
        obj = Comment.objects.get(id = comId)
        obj.reply = message
        obj.save()
    except:
        return JsonResponse(data={'error':'Xəta baş verdi'})
    return JsonResponse(data={'msg':obj.reply,'cid':obj.id})

@login_required
def shareView(request):
    print(request)
    fileId=request.GET.get('fileId')
    username=request.GET.get('username')
    try:
        fileForm=MyFile.objects.get(id=fileId)
        user=User.objects.get(username=username)
    except:
        return JsonResponse(data={'error':'Fayl ve ya istifadəçi tapılmadı'})

    fileForm.can_see.add(user)
    return JsonResponse(data={'info':'ugurlu'})
    
@login_required
def sharedPeopleView(request, id):
    obj = MyFile.objects.get(id = id)
    if request.user == obj.user:
        people  = obj.can_see.all()



        return render(request, 'shared_people.html', context={
            'people': people,
            'fileId': obj.id
        })
    else:
        return redirect('empty:home')
@login_required
def delSharedPeopleView(request):
    fileId = request.GET.get('fileid')
    personId = request.GET.get('userid')
    try:
        user = User.objects.get(id = personId)
        file = MyFile.objects.get(id = fileId)
        file.can_see.remove(user)
    except:
        return JsonResponse(data = {
        'error': 'Xeta bas verdi',
        })
    return JsonResponse(data = {
        'info': 'Istifadeci gorebilenlerden silindi',
    })

@login_required
def comment_permissionView(request):
    fileId = request.GET.get("fileId")
    obj = MyFile.objects.get(id = fileId)
    if obj.publish_comment:

        obj.publish_comment = False
       
        
    else:
        obj.publish_comment = True

    obj.save() 
    
    if obj.publish_comment:

        return JsonResponse(data={
        'permission': True
        })

    return JsonResponse(data={
        'permission': False
    })
