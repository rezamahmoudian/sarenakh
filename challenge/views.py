from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from rest_framework import status
from .models import *
from typing import Dict


# Create your views here.


def response_func(status: bool, msg: str, data: Dict) -> Dict:
    res = {
        'status': status,
        'message': msg,
        'data': data
    }
    return res


class HomeAPIView(generics.GenericAPIView):
    serializer_class = (HomeSerializer,)

    def get(self, request):

        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)

        medias = [{
            "id": 1,
            "address": "media",
            "model": "challenge"
        },
            {
                "id": 2,
                "address": "media",
                "model": "challenge"
            },
            {
                "id": 3,
                "address": "media",
                "model": "challenge"
            }
        ]
        # medias = request.data
        # print(medias)
        data = []

        for media in medias:
            if media['model'] == "challenge":
                print(media['id'])
                user_mission = UserMission.objects.get(video_id=media['id'])
                # user_challenge = UserChallenge.objects.get(challenge_id=user_mission.challenge_id)
                # mission = Mission.objects.get(id=user_mission.mission_id.id)

                media_data = {
                    "address": media["address"],
                    "mission_order": user_mission.mission_id.mission_order,
                    "time": user_mission.time,
                    "user_id": "",
                    "profile": "",
                    "name": "",
                    "family": ""
                }

                data.append(media_data)

        return Response(
            response_func(True, 'OK', data),
            status=status.HTTP_200_OK
        )


class ChallengesAPIView(generics.GenericAPIView):

    def get(self, request):
        data = []
        challenges = Challenge.objects.all().order_by('-id')
        print(challenges)
        for challenge in challenges:
            print(challenge)
            challenge_data = {
                "id": challenge.id,
                "name": challenge.name,
                "price": challenge.enter_price,
                "start_time": challenge.start_time,
                "end_time": challenge.end_time,
                "status": challenge.status,

            }
            data.append(challenge_data)
        return Response(
            response_func(True, 'OK', data),
            status=status.HTTP_200_OK
        )


class ChallengesDetailAPIView(generics.GenericAPIView):
    def get(self, request, id):
        challenge = Challenge.objects.get(id=id)
        print(challenge)
        data = {
            "id": challenge.id,
            "name": challenge.name,
            "price": challenge.enter_price,
            "start_time": challenge.start_time,
            "end_time": challenge.end_time,
            "attended_number": challenge.attended_number,
            "mission_count": challenge.mission_count,
            "difficulty": challenge.difficulty,
            "reward_price": challenge.reward_price,
            "description": challenge.description,
            "status": challenge.status,
        }

        return Response(
            response_func(True, 'OK', data),
            status=status.HTTP_200_OK
        )

    def post(self, request, id):
        # yones
        user_id = 10
        challenge = Challenge.objects.get(id=id)

        user_challenge = UserChallenge.objects.create(user_id=user_id, challenge=challenge)
        user_challenge.save()

        challenge.attended_number += 1
        challenge.save()

        return Response(
            response_func(True, 'OK', {}),
            status=status.HTTP_200_OK
        )


class ChallengesDetailUserAPIView(generics.GenericAPIView):
    def get(self, request, id, user_id):
        challenge = Challenge.objects.get(id=id)
        print(challenge)
        user_challenge_status = False
        user_challenges = UserChallenge.objects.filter(challenge=challenge).order_by('current_mission')

        top_players = []
        for user in user_challenges:
            top_players.append(user.user_id)

        try:
            user_challenge = user_challenges.get(user_id=user_id)
            # user_challenge = UserChallenge.objects.get(user_id=user_id, challenge=challenge)
            if user_challenge:
                user_challenge_status = True
            else:
                user_challenge_status = False
        except:
            pass

        data = {
            "id": challenge.id,
            "name": challenge.name,
            "price": challenge.enter_price,
            "start_time": challenge.start_time,
            "end_time": challenge.end_time,
            "attended_number": challenge.attended_number,
            "mission_count": challenge.mission_count,
            "difficulty": challenge.difficulty,
            "reward_price": challenge.reward_price,
            "description": challenge.description,
            "status": challenge.status,
        }

        return Response(
            response_func(True, 'OK', data),
            status=status.HTTP_200_OK
        )

    def post(self, request, id):
        # yones
        user_id = 10
        challenge = Challenge.objects.get(id=id)

        user_challenge = UserChallenge.objects.create(user_id=user_id, challenge=challenge)
        user_challenge.save()

        challenge.attended_number += 1
        challenge.save()

        return Response(
            response_func(True, 'OK', {}),
            status=status.HTTP_200_OK
        )

class ChallengesShowAPIView(generics.GenericAPIView):
    def get(self, request, id):
        # yones
        user_id = 1
        challenge = Challenge.objects.get(id=id)
        user_challenges = UserChallenge.objects.all()
        user_challenge = user_challenges.get(challenge=challenge, user_id=user_id)
        mission = user_challenge.current_mission

        user_ids = []
        users = user_challenges.filter(challenge=challenge, current_mission=mission)
        for user in users:
            user_ids.append(user.user_id)

        data = {
            "mission_name": mission.name,
            "mission_description": mission.description,
            "mission_type": mission.mission_type,
            "user_ids": user_ids
        }

        return Response(
            response_func(True, 'OK', data),
            status=status.HTTP_200_OK
        )


class ChallengesUpdateAPIView(generics.GenericAPIView):

    def post(self, request, id):
        # yones
        user_id = 1
        answer = request.data['answer']

        challenge = Challenge.objects.get(id=id)

        user_challenge = UserChallenge.objects.get(user_id=user_id, challenge=challenge)
        mission = user_challenge.current_mission
        user_mission = UserMission.objects.get(user_id=user_id, challenge_id=id, mission_id=mission)
        answers_json = mission.correct_answers
        print(answers_json)

        if mission.mission_type == 1:

            for ans in list(answers_json):
                if answer == ans:
                    user_mission.acceptance = 3
                    user_mission.save()
                    if mission.id < challenge.mission_count:
                        new_mission = Mission.objects.get(id=mission.id+1)
                        user_challenge.current_mission = new_mission
                        user_challenge.save()
                        # new_user_mission = UserMission.objects.create(user_id=user_id, mission_id=new_mission, challenge=user_challenge, )

                        return Response(
                            response_func(True, 'مرحله با موفقیت پشت سر گداشته شد', {}),
                            status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            response_func(True, 'تبریک شما با موفقیت همه ی مراحل را پشت سر گذاشتید', {}),
                            status=status.HTTP_200_OK
                        )
                else:
                    return Response(
                        response_func(True, 'پاسخ ارسالی اشتباه است', {}),
                        status=status.HTTP_200_OK
                    )
        else:
            msg = "لطفا منتظر تایید ویدوی ارسالی بمانید"
            user_mission.acceptance = 2
            user_mission.save()

            return Response(
                response_func(True, msg, {}),
                status=status.HTTP_200_OK
            )
