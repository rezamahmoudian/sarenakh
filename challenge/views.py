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
        data = []
        user_missions = UserMission.objects.filter(acceptance=3, video_id__gt=0)

        for user_mission in user_missions:

            user_mission_data = {
                "user_id": user_mission.user_id,
                # "mission_id": user_mission.mission_id.id,
                "time": user_mission.time,
                "video_id": user_mission.video_id,
                "challenge_name": user_mission.challenge.name,
                "mission_name": user_mission.mission_id.name,
                "video_like": user_mission.like_video
            }

            data.append(user_mission_data)

        return Response(
            response_func(True, 'OK', data),
            status=status.HTTP_200_OK
        )
class ProfileAPIView(generics.GenericAPIView):

    def get(self, request, user_id):
        data = []
        user_missions = UserMission.objects.filter(acceptance=3, video_id__gt=0, user_id=user_id)

        for user_mission in user_missions:

            user_mission_data = {
                "user_id": user_mission.user_id,
                # "mission_id": user_mission.mission_id.id,
                "time": user_mission.time,
                "video_id": user_mission.video_id,
                "challenge_name": user_mission.challenge.name,
                "mission_name": user_mission.mission_id.name,
                "video_like": user_mission.like_video
            }

            data.append(user_mission_data)

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


# class ChallengesDetailAPIView(generics.GenericAPIView):
#     def get(self, request, id):
#         challenge = Challenge.objects.get(id=id)
#         print(challenge)
#         data = {
#             "id": challenge.id,
#             "name": challenge.name,
#             "price": challenge.enter_price,
#             "start_time": challenge.start_time,
#             "end_time": challenge.end_time,
#             "attended_number": challenge.attended_number,
#             "mission_count": challenge.mission_count,
#             "difficulty": challenge.difficulty,
#             "reward_price": challenge.reward_price,
#             "description": challenge.description,
#             "status": challenge.status,
#         }
#
#         return Response(
#             response_func(True, 'OK', data),
#             status=status.HTTP_200_OK
#         )
#
#     def post(self, request, id):
#         # yones
#         user_id = 10
#         challenge = Challenge.objects.get(id=id)
#
#         user_challenge = UserChallenge.objects.create(user_id=user_id, challenge=challenge)
#         user_challenge.save()
#
#         challenge.attended_number += 1
#         challenge.save()
#
#         return Response(
#             response_func(True, 'OK', {}),
#             status=status.HTTP_200_OK
#         )


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
            "difficulty": DIFFICULTY_CHOICES[challenge.difficulty-1][1],
            "reward_price": challenge.reward_price,
            "description": challenge.description,
            "status": challenge.status,
            "top_players": top_players,
            "user_challenge_status": user_challenge_status
        }

        return Response(
            response_func(True, 'OK', data),
            status=status.HTTP_200_OK
        )

    def post(self, request, id, user_id):
        user_id = user_id
        challenge = Challenge.objects.get(id=id)
        mission = Mission.objects.get(challenge=challenge, mission_order=1)

        user_challenge, bool = UserChallenge.objects.get_or_create(user_id=user_id, challenge=challenge, current_mission=mission)

        if bool == True:
            user_challenge.current_mission = mission
            user_challenge.save()
            challenge.attended_number += 1
            challenge.save()

            return Response(
                response_func(True, 'با موفقیت ثبتنام کردید', {}),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                response_func(True, 'شما قبلا در این مسابقه ثبتنام کرده اید.لطفا وارد مسابقه شوید', {}),
                status=status.HTTP_200_OK
            )


class ChallengesShowAPIView(generics.GenericAPIView):
    def get(self, request, id, user_id):
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
    def post(self, request, id, user_id):
        try:
            answer = request.data['answer']

            level = Level.objects.get(user_id=user_id)
            challenge = Challenge.objects.get(id=id)

            user_challenge = UserChallenge.objects.get(user_id=user_id, challenge=challenge)
            mission = user_challenge.current_mission
            user_mission, create_bool = UserMission.objects.get_or_create(user_id=user_id, challenge_id=challenge.id, mission_id=mission)

            answers_json = mission.correct_answers
            answer_is_correct = False

            if mission.mission_type == 1:

                for ans in answers_json:

                    if (answer == answers_json[ans]) and ( user_mission.acceptance != 3):
                        answer_is_correct = True

                        user_mission.acceptance = 3
                        user_mission.save()

                        final_xp = level.xp + mission.difficulty

                        if final_xp < level.max_xp:
                            level.xp += mission.difficulty * 10

                        else:
                            level.xp = (level.xp + mission.difficulty * 10) - level.max_xp
                            level.level += 1
                        level.save()

                        if mission.mission_order < challenge.mission_count:
                            new_mission = Mission.objects.get(id=mission.id + 1)
                            user_challenge.current_mission = new_mission
                            user_challenge.save()
                            # new_user_mission = UserMission.objects.create(user_id=user_id, mission_id=new_mission, challenge=user_challenge, )

                            return Response(
                                response_func(True, 'مرحله با موفقیت پشت سر گذاشته شد', {}),
                                status=status.HTTP_200_OK
                            )
                        else:
                            return Response(
                                response_func(True, 'تبریک. شما این مسابقه را با موفقیت به اتمام رساندید', {}),
                                status=status.HTTP_200_OK
                            )
                #         bayad current mission check she on dorost tare
                # if user_mission.acceptance == 3:
                #     return Response(
                #         response_func(True, "شما این مرحله را قبلا پشت سر گذاشته اید", {}),
                #         status=status.HTTP_200_OK
                #     )
                if answer_is_correct == False:
                    return Response(
                        response_func(True, "پاسخ ارسالی اشتباه است", {}),
                        status=status.HTTP_200_OK
                    )
            else:
                if request.data['video_id'] and request.data['img_id']:
                    video_id = request.data['video_id']
                    image_id = request.data['img_id']
                    user_mission.image_id = image_id
                    user_mission.video_id = video_id
                    user_mission.save()

                elif request.data['video_id']:
                    video_id = request.data['video_id']
                    user_mission.video_id = video_id
                    user_mission.save()

                elif request.data['image_id']:
                    image_id = request.data['img_id']
                    user_mission.image_id = image_id
                    user_mission.save()


                msg = "لطفا منتظر تایید ویدوی ارسالی بمانید"
                user_mission.acceptance = 2
                user_mission.save()

                return Response(
                    response_func(True, msg, {}),
                    status=status.HTTP_200_OK
                )

        except:
            return Response(
                response_func(False, "شما امکان شرکت در این مرحله را ندارید", {}),
                status=status.HTTP_400_BAD_REQUEST
            )
