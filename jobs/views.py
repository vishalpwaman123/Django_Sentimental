from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
import moviepy.editor as mp
import wave
import math
import glob
import speech_recognition as sr
import os
from textblob import TextBlob
from pydub import AudioSegment

mp3_extension = '.mp3'
ogg_extension = '.ogg'
wav_extension = '.wav'
destination_Location = "media/finalWavResult.wav"
Current_Extension = None


def main(request):
    return render(request, 'jobs/main.html')


def result(request):
    return render(request, 'jobs/result.html')


def home(request):
    return render(request, 'jobs/home.html')


def my_file(a, file):
    with open(file+'.txt', mode='a') as f:
        f.write(a+'\n')
    f.close()


def vender(file):
    context1 = {}

    pos_count = 0
    pos_correct = 0

    with open(file+".txt", "r") as f:
        for line in f.read().split('\n'):
            analysis = TextBlob(line)

            if analysis.sentiment.subjectivity > 0.5:
                if analysis.sentiment.polarity > 0:
                    pos_correct += 1
                pos_count += 1

    neg_count = 0
    neg_correct = 0

    with open(file+".txt", "r") as f:
        for line in f.read().split('\n'):
            analysis = TextBlob(line)
            if analysis.sentiment.subjectivity > 0.5:
                if analysis.sentiment.polarity <= 0:
                    neg_correct += 1
                neg_count += 1

    try:
        print("Positive accuracy = {}% via {} samples".format(
            pos_correct/pos_count*100.0, pos_count))

        context1['Positive'] = (pos_correct/pos_count*100.0)

    except ZeroDivisionError as error:
        print("Divide by zero exception")

    try:
        print("Negative accuracy = {}% via {} samples".format(
            neg_correct/neg_count*100.0, neg_count))

        context1['Negative'] = (neg_correct/neg_count*100.0)

    except ZeroDivisionError as error:
        print("Divide by zero exception")

    f.close()

    return context1


def audio(request):
    print("Flag1")
    # context = {}
    context1 = {}
    r = sr.Recognizer()  				# Create Object
    if request.method == 'POST':  		# Recognize POST method
        print("Flag2")
        upload = request.FILES['document']  # Fetch File From Front End
        fs = FileSystemStorage()  # Create File Storage Object
        name = fs.save(upload.name, upload)  # Save File In File Storage
        print(name)
        # context['url']=fs.url(name)
        mp4_files = glob.glob('media/'+upload.name)  # Save File At media/
        for m in mp4_files:  # Looping Start
            print("Flag3")
            file, extension = os.path.splitext(
                m)  # Split File Name & Extension
            Current_Extension = extension
            print(extension)
            # Create Object Using Path With Audio File

            try:

                if mp3_extension == extension:
                    conversion_Sound = AudioSegment.from_mp3(
                        'media/'+upload.name)
                    conversion_Sound.export(destination_Location, format="wav")
                elif ogg_extension == extension:
                    conversion_Sound = AudioSegment.from_ogg(
                        'media/'+upload.name)
                    conversion_Sound.export(destination_Location, format="wav")
                elif wav_extension == extension:
                    conversion_Sound = AudioSegment.from_wav(
                        'media/'+upload.name)
                    conversion_Sound.export(destination_Location, format="wav")
                else:
                    conversion_Sound = AudioSegment.from_file(
                        'media/'+upload.name)
                    conversion_Sound.export(destination_Location, format="wav")

            except Exception as e:
                print("Unwanted file Conversion Error occure {0}".format(e))

            try:
                # Open File And Read File
                origAudio = wave.open(destination_Location, 'r')
            except FileNotFoundError:
                print("You don't have this file , bro")

            onair = sr.AudioFile('media/finalWavResult.wav')
            frameRate = origAudio.getframerate()  # Calculate Frame Rate
            n_frames = origAudio.getnframes()  # Calculate Number Of frames
            song_length = n_frames/frameRate  # Calculate Length Of Song
            os.remove('{0}'.format(file)+Current_Extension)
            print("Total length of speech :")
            print(song_length)
            print("")
            clip_len = 7
            # Song Divide Number Of Part
            n_clips = math.floor(song_length/clip_len)
            print("No of sub part Create :")
            print(n_clips)
            print("")
            print(conversion_Sound)
            Line_Number = 1
            with onair as source:
                while(n_clips >= 40):

                    try:
                        # Record Audio
                        audio = r.record(source, duration=clip_len)
                        try:
                            a = r.recognize_google(
                                audio)  # REcognize Audio
                        except sr.UnknownValueError as e:
                            print("Could not understand audio")
                        except sr.RequestError as e:
                            print(
                                "Could not request results; {0}".format(e))
                        print(str(Line_Number)+' : '+a)
                        my_file(a, file)
                    except sr.UnknownValueError:
                        print("Could not understand audio")
                    except sr.RequestError as e:
                        print("Could not request results; {0}".format(e))

                    print("------------------------------------------------")
                    Line_Number = Line_Number+1
                    n_clips = n_clips-1

        origAudio.close()
        os.remove(destination_Location)
        context1 = vender(file)
        os.remove('{}.txt'.format(file))
        # os.remove('{0}.{1}'.format(file) .format(Current_Extension))
    if len(context1) == 0:
        return render(request, 'jobs/audio.html', context1)
    else:
        return render(request, 'jobs/result.html', context1)


def video(request):

    print("VFlag1")
    context1 = {}
    context = {}
    r = sr.Recognizer()
    if request.method == 'POST':
        print("VFlag2")
        upload = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(upload.name, upload)
        context['url'] = fs.url(name)
        # os.remove('media/*')
        mp4_files = glob.glob('media/'+upload.name)
        for m in mp4_files:
            print("VFlag3")
            file, extension = os.path.splitext(m)
            print(file)
            print(extension)
            my_clip = mp.VideoFileClip(r'media/'+upload.name)
            my_clip.audio.write_audiofile(file+".wav")
            my_clip.close()

            os.remove('{}.mp4'.format(file))
            print('"{}" successfully converted into wav!'.format(m))
            print("")
            print("")
            path = file+'.wav'
            print(path)
            onair = sr.AudioFile(path)
            print("You have No Exception: , bro")
            try:
                origAudio = wave.open(path, 'r')  # Open File And Read File
            except FileNotFoundError:
                print("You don't have this file , bro")
            frameRate = origAudio.getframerate()
            n_frames = origAudio.getnframes()
            song_length = n_frames/frameRate

            print("Total length of speech :")
            print(song_length)
            print("")
            clip_len = 10
            n_clips = math.floor(song_length/clip_len)
            print("No of sub part Create :")
            print(n_clips)
            print("")
            print(onair)
            with onair as source:
                while(n_clips >= 0):
                    try:
                        audio = r.record(source, duration=clip_len)
                        try:
                            a = r.recognize_google(audio)  # REcognize Audio
                        except sr.UnknownValueError as e:
                            print("Could not understand audio")
                        except sr.RequestError as e:
                            print("Could not request results; {0}".format(e))
                        print(n_clips+' '+a)
                        my_file(a, file)
                    except sr.UnknownValueError:
                        print("Could not understand audio")
                    except sr.RequestError as e:
                        print("Could not request results; {0}".format(e))

                    print("------------------------------------------------")
                    n_clips = n_clips-1

            origAudio.close()
            os.remove('{}.wav'.format(file))
            vender(file)
            context1 = vender(file)
            os.remove('{}.txt'.format(file))
    if len(context1) == 0:
        return render(request, 'jobs/video.html', context1)
    else:
        return render(request, 'jobs/result.html', context1)


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password1']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'analysis/signup.html', {'error': 'Username is All ready taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password'])
                auth.login(request, user)
                return redirect('login')
        else:
            return render(request, 'jobs/signup.html', {'error': 'password does\'t matched'})
    else:
        return render(request, 'jobs/signup.html')

    return render(request, 'jobss/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST.get(
            'username1'), password=request.POST.get('password'))
        if user is not None:
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'jobs/signin.html', {'error': 'username AND password incorrect'}, {'username', username}, {'password': password})
    else:
        return render(request, 'jobs/signin.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
