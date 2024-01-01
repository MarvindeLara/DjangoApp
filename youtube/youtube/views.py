import json
from random import random

from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from youtube.forms import VideoForm
from youtube.models import Video, Playlist


def index(request):
    # if request.method == 'GET' and 'key' in request.GET:
    #     key = request.GET['key']
    #     if key is not None and key != '':
    #         videos = Video.objects.filter(title__icontains=key)
    #         print(videos)
    #     else:
    #         videos = Video.objects.all()
    # else:
    videos = Video.objects.all()

    all_videos = []
    row_video = {'col1': None, 'col2': None, 'col3': None}

    for video in videos:

        html_video = {}
        html_video['id'] = video.id
        html_video['title'] = video.title
        html_video['description'] = video.description
        html_video['views'] = video.views
        # html_video['user'] = model_to_dict(video.user)
        html_video['user'] = video.user
        html_video['added'] = video.added
        html_video['source'] = "http://img.youtube.com/vi/" + video.source.split('?')[0].split('/')[-1] + "/hqdefault.jpg"
        # "http://img.youtube.com/vi/K5PXiNpvfX0/hqdefault.jpg" https://www.youtube.com/embed/K5PXiNpvfX0?si=qZL7BfYLtuXQ_4p1
        video = html_video

        if not row_video['col1']:
            row_video['col1'] = video
        elif not row_video['col2']:
            row_video['col2'] = video
        else:
            row_video['col3'] = video
            all_videos.append(row_video)
            row_video = {'col1': None, 'col2': None, 'col3': None}

    if row_video['col1']:  # for last incomplete row
        all_videos.append(row_video)

    return render(request, 'youtube/index.html', {'videos': all_videos})


def search_results(request):
    if request.method == 'GET' and 'key' in request.GET:
        key = request.GET['key']
        if key is not None and key != '':
            videos = Video.objects.filter(title__icontains=key)
            # print(videos)
        else:
            videos = Video.objects.all()
    else:
        videos = Video.objects.all()

    all_videos = []
    row_video = {'col1': None, 'col2': None, 'col3': None}

    for video in videos:

        html_video = {}
        html_video['id'] = video.id
        html_video['title'] = video.title
        html_video['description'] = video.description
        html_video['views'] = video.views
        # html_video['user'] = model_to_dict(video.user)
        html_video['user'] = video.user
        html_video['added'] = video.added
        html_video['source'] = "http://img.youtube.com/vi/" + video.source.split('?')[0].split('/')[-1] + "/hqdefault.jpg"
        # "http://img.youtube.com/vi/K5PXiNpvfX0/hqdefault.jpg" https://www.youtube.com/embed/K5PXiNpvfX0?si=qZL7BfYLtuXQ_4p1
        video = html_video

        if not row_video['col1']:
            row_video['col1'] = video
        elif not row_video['col2']:
            row_video['col2'] = video
        else:
            row_video['col3'] = video
            all_videos.append(row_video)
            row_video = {'col1': None, 'col2': None, 'col3': None}

    if row_video['col1']:  # for last incomplete row
        all_videos.append(row_video)

    if request.method == 'GET' and 'key' in request.GET:
        # videos = {}
        # html = ''
        # #################################################################################
        # # create the new html text here that will replace <div id="videos"> contents
        # html = html + """<h1 class ="fw-normal text-center">Welcome</h1>"""
        # #################################################################################
        # videos['html'] = html
        # return HttpResponse(
        #     json.dumps(videos, default=str),
        #     content_type="application/json"
        # )
        return render(request, 'youtube/index_results.html', {'videos': all_videos})
    else:
        return render(request, 'youtube/index_results.html', {'videos': all_videos})


def video_view(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.views = video.views + 1
    video.save()
    video_viewed = get_object_or_404(Video, pk=pk)
    video_viewed.source = video_viewed.source + "&autoplay=1"

    videos = Video.objects.all()

    all_videos = []
    row_video = {'col1': None, 'col2': None, 'col3': None}

    for video in videos:
        if video.id == pk:
            continue

        html_video = {}
        html_video['id'] = video.id
        html_video['title'] = video.title
        html_video['description'] = video.description
        html_video['views'] = video.views
        html_video['user'] = video.user
        html_video['added'] = video.added
        html_video['source'] = "http://img.youtube.com/vi/" + video.source.split('?')[0].split('/')[
            -1] + "/hqdefault.jpg"
        # "http://img.youtube.com/vi/K5PXiNpvfX0/hqdefault.jpg" https://www.youtube.com/embed/K5PXiNpvfX0?si=qZL7BfYLtuXQ_4p1
        video = html_video

        if not row_video['col1']:
            row_video['col1'] = video
        elif not row_video['col2']:
            row_video['col2'] = video
        else:
            row_video['col3'] = video
            all_videos.append(row_video)
            row_video = {'col1': None, 'col2': None, 'col3': None}

    if row_video['col1']:  # for last incomplete row
        all_videos.append(row_video)

    return render(request, 'youtube/video_view.html', {'video': video_viewed, 'videos': all_videos})


# @login_required
def video_like(request, pk):
    if isinstance(request.user, AnonymousUser):
        video_viewed_json = {}
        video_viewed_json['status'] = 0
        # video_viewed_json['likes'] = video_viewed.likes
        return HttpResponse(
            json.dumps(video_viewed_json),
            content_type="application/json"
        )

    video = get_object_or_404(Video, pk=pk)
    video.likes = video.likes + 1
    video.save()
    video_viewed = get_object_or_404(Video, pk=pk)

    video_viewed_json = {}
    video_viewed_json['status'] = 1
    video_viewed_json['likes'] = video_viewed.likes
    return HttpResponse(
        json.dumps(video_viewed_json),
        content_type="application/json"
    )


@login_required
def video_myvideos(request):
    videos = Video.objects.filter(user=request.user)

    my_videos = []
    row_video = {'col1': None, 'col2': None, 'col3': None}

    for video in videos:

        html_video = {}
        html_video['id'] = video.id
        html_video['title'] = video.title
        html_video['description'] = video.description
        html_video['views'] = video.views
        html_video['user'] = video.user
        html_video['added'] = video.added
        html_video['source'] = "http://img.youtube.com/vi/" + video.source.split('?')[0].split('/')[
            -1] + "/hqdefault.jpg"
        # "http://img.youtube.com/vi/K5PXiNpvfX0/hqdefault.jpg" https://www.youtube.com/embed/K5PXiNpvfX0?si=qZL7BfYLtuXQ_4p1
        video = html_video

        if not row_video['col1']:
            row_video['col1'] = video
        elif not row_video['col2']:
            row_video['col2'] = video
        else:
            row_video['col3'] = video
            my_videos.append(row_video)
            row_video = {'col1': None, 'col2': None, 'col3': None}

    if row_video['col1']:  # for last incomplete row
        my_videos.append(row_video)

    return render(request, 'youtube/video_myvideos.html', {'videos': my_videos})


@login_required
def video_new(request):
    form = VideoForm(request.POST or None)

    if form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        # messages.success(request, 'Added new video')
        return redirect('youtube:video_myvideos')

    return render(request, 'youtube/video_form.html', {'form': form})


@login_required
def video_edit(request, pk):
    video = get_object_or_404(Video, pk=pk, user=request.user)
    form = VideoForm(request.POST or None, instance=video)

    if form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        # messages.success(request, 'Updated video')
        return redirect('youtube:video_myvideos')

    return render(request, 'youtube/video_form.html', {'video': video, 'form': form})


@login_required
def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk, user=request.user)
    video.source = video.source + "&autoplay=1"

    if request.method == 'POST':
        video.delete()
        # messages.success(request, 'Deleted video')
        return redirect('youtube:video_myvideos')

    return render(request, 'youtube/video_confirm_delete.html', {'video': video})


def video_addtoplaylist(request, pk):
    if isinstance(request.user, AnonymousUser):
        video_viewed_json = {}
        video_viewed_json['status'] = 0
        return HttpResponse(
            json.dumps(video_viewed_json),
            content_type="application/json"
        )

    video = get_object_or_404(Video, pk=pk)
    video_addedtoplaylist = Playlist.objects.filter(user=request.user, video=video)
    video_viewed_json = {}
    video_viewed_json['message'] = "Video is already in playlist."
    if not video_addedtoplaylist:
        video_addedtoplaylist = Playlist()
        video = get_object_or_404(Video, pk=pk)
        video_addedtoplaylist.user = request.user
        video_addedtoplaylist.video = video
        video_addedtoplaylist.save()
        video_viewed_json['message'] = "Video is added to playlist."
        # messages.success(request, 'Added new video in playlist')

    video_viewed_json['status'] = 1
    return HttpResponse(
        json.dumps(video_viewed_json),
        content_type="application/json"
    )


@login_required
def video_myplaylist(request):
    playlist = Playlist.objects.filter(user=request.user)

    my_videos = []
    row_video = {'col1': None, 'col2': None, 'col3': None}

    for item in playlist:
        video = item.video
        html_video = {}
        html_video['id'] = video.id
        html_video['title'] = video.title
        html_video['description'] = video.description
        html_video['views'] = video.views
        html_video['user'] = video.user
        html_video['added'] = video.added
        html_video['source'] = "http://img.youtube.com/vi/" + video.source.split('?')[0].split('/')[
            -1] + "/hqdefault.jpg"
        # "http://img.youtube.com/vi/K5PXiNpvfX0/hqdefault.jpg" https://www.youtube.com/embed/K5PXiNpvfX0?si=qZL7BfYLtuXQ_4p1
        video = html_video

        if not row_video['col1']:
            row_video['col1'] = video
        elif not row_video['col2']:
            row_video['col2'] = video
        else:
            row_video['col3'] = video
            my_videos.append(row_video)
            row_video = {'col1': None, 'col2': None, 'col3': None}

    if row_video['col1']:  # for last incomplete row
        my_videos.append(row_video)

    return render(request, 'youtube/video_myplaylist.html', {'videos': my_videos})


@login_required
def video_addtoplaylist_fromindex(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video_addedtoplaylist = Playlist.objects.filter(user=request.user, video=video)
    if not video_addedtoplaylist:
        video_addedtoplaylist = Playlist()
        video = get_object_or_404(Video, pk=pk)
        video_addedtoplaylist.user = request.user
        video_addedtoplaylist.video = video
        video_addedtoplaylist.save()
        # messages.success(request, 'Added new video in playlist')

    playlist = Playlist.objects.filter(user=request.user)

    my_videos = []
    row_video = {'col1': None, 'col2': None, 'col3': None}

    for item in playlist:
        video = item.video
        html_video = {}
        html_video['id'] = video.id
        html_video['title'] = video.title
        html_video['description'] = video.description
        html_video['views'] = video.views
        html_video['user'] = video.user
        html_video['added'] = video.added
        html_video['source'] = "http://img.youtube.com/vi/" + video.source.split('?')[0].split('/')[
            -1] + "/hqdefault.jpg"
        # "http://img.youtube.com/vi/K5PXiNpvfX0/hqdefault.jpg" https://www.youtube.com/embed/K5PXiNpvfX0?si=qZL7BfYLtuXQ_4p1
        video = html_video

        if not row_video['col1']:
            row_video['col1'] = video
        elif not row_video['col2']:
            row_video['col2'] = video
        else:
            row_video['col3'] = video
            my_videos.append(row_video)
            row_video = {'col1': None, 'col2': None, 'col3': None}

    if row_video['col1']:  # for last incomplete row
        my_videos.append(row_video)

    return render(request, 'youtube/video_myplaylist.html', {'videos': my_videos})


@login_required
def video_deletefromplaylist(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.source = video.source + "&autoplay=1"

    if request.method == 'POST':
        video = get_object_or_404(Video, pk=pk)
        videoplaylist = get_object_or_404(Playlist, user=request.user, video=video)
        videoplaylist.delete()
        # messages.success(request, 'Deleted video from playlist')
        return redirect('youtube:video_myplaylist')

    return render(request, 'youtube/videoplaylist_confirm_delete.html', {'video': video})



