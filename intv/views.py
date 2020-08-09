from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll, Question, Answer
from .serializers import PollSerializer, QuestionSerializer, AnswerSerializer


class PollListView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        polls = Poll.objects.all()
        serialized = PollSerializer(polls, many=True).data
        return Response({"polls": serialized}, status=status.HTTP_200_OK)


class PollAddView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        serializer = PollSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Created successfully"}, status.HTTP_200_OK)


class PollEditView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        if "id" not in request.query_params:
            return Response("Please, specify the id", status=status.HTTP_400_BAD_REQUEST)
        if "start_date" in request.query_params:
            return Response("start_date can't be edit", status=status.HTTP_400_BAD_REQUEST)
        saved_poll = get_object_or_404(Poll.objects.filter(id=request.query_params["id"]))
        serializer = PollSerializer(instance=saved_poll, data=request.query_params, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Updated successfully"}, status.HTTP_200_OK)


class PollDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        if "id" not in request.query_params:
            return Response("Please, specify the id", status=status.HTTP_400_BAD_REQUEST)
        poll = get_object_or_404(Poll.objects.filter(id=request.query_params["id"]))
        poll.delete()
        return Response({"success": "Deleted successfully"}, status.HTTP_200_OK)


class QuestionListView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        questions = Question.objects.all()
        serialized = QuestionSerializer(questions, many=True).data
        return Response({"questions": serialized}, status.HTTP_200_OK)


class QuestionAddView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        if "poll_id" not in request.query_params:
            return Response("Please, specify the poll_id", status=status.HTTP_400_BAD_REQUEST)
        poll = Poll.objects.filter(id=request.query_params["poll_id"])
        serialized = PollSerializer(poll, many=True).data
        if not serialized:
            return Response("Please, specify the right poll_id", status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Created successfully"}, status.HTTP_200_OK)


class QuestionEditView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        if "id" not in request.query_params:
            return Response("Please, specify the id", status=status.HTTP_400_BAD_REQUEST)
        saved_question = get_object_or_404(Question.objects.filter(id=request.query_params["id"]))
        serializer = QuestionSerializer(instance=saved_question, data=request.query_params, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Updated successfully"}, status.HTTP_200_OK)


class QuestionDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        if "id" not in request.query_params:
            return Response("Please, specify the id", status=status.HTTP_400_BAD_REQUEST)
        question = get_object_or_404(Question.objects.filter(id=request.query_params["id"]))
        question.delete()
        return Response({"success": "Deleted successfully"}, status.HTTP_200_OK)


class PollsGetView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        polls = Poll.objects.all()
        questions = Question.objects.all()
        serialized_polls = PollSerializer(polls, many=True).data
        serialized_questions = QuestionSerializer(questions, many=True).data
        data = []
        for item in serialized_polls:
            array = [item]
            for i in serialized_questions:
                print(i)
                if i["poll_id"] == item["id"]:
                    array.append(i)
            data.append(array)
        return Response({"Polls": data}, status.HTTP_200_OK)


class AnswerAddView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = AnswerSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            pass
        question = Question.objects.filter(id=request.query_params["question_id"])
        serialized_question = QuestionSerializer(question, many=True).data
        if not serialized_question:
            return Response("Please, specify the right question_id", status=status.HTTP_400_BAD_REQUEST)
        answer = Answer.objects.filter(user_id=request.query_params["user_id"],
                                       question_id=request.query_params["question_id"])
        serialized_answer = AnswerSerializer(answer, many=True).data
        if serialized_answer:
            return Response("You have already voted", status=status.HTTP_400_BAD_REQUEST)
        question_type = serialized_question[0]["type"]
        if question_type == "YN":
            if request.query_params["answer"] != "Yes" and request.query_params["answer"] != "No":
                return Response("Answer must be Yes or No", status=status.HTTP_400_BAD_REQUEST)
        elif question_type == "VALUES":
            values = serialized_question[0]["values"].split(",")
            if request.query_params["answer"] not in values:
                return Response("Answer must be one of values", status=status.HTTP_400_BAD_REQUEST)

        serializer = AnswerSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Created successfully"}, status.HTTP_200_OK)


class AnswerListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if "user_id" not in request.query_params:
            return Response("Please, specify the user_id", status=status.HTTP_400_BAD_REQUEST)
        answers = Answer.objects.filter(user_id=request.query_params["user_id"])
        serialized = AnswerSerializer(answers, many=True).data
        return Response({"Answer": serialized}, status.HTTP_200_OK)
