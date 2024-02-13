from rest_framework import status
from rest_framework.response import Response


def _create_response_not_valid_user_credentials_and_serializers(exceptions):
    # a = FailedResponse(status=status.HTTP_400_BAD_REQUEST, message=...)
    return Response(
        {"status": "failed", "message": exceptions.detail["non_field_errors"][0]},
        status=status.HTTP_400_BAD_REQUEST,
    )


def _create_response_not_valid_token(exception):
    return Response(
        {"status": "failed", "message": exception.detail["detail"]},
        status=status.HTTP_400_BAD_REQUEST,
    )


def _create_response_not_found(exception):
    return Response(
        {"status": "failed", "message": str(exception.message)},
        status=status.HTTP_404_NOT_FOUND,
    )


def _create_response_for_exception(exception):
    return Response(
        {"status": "failed", "message": str(exception.message)},
        status=status.HTTP_400_BAD_REQUEST,
    )


def _create_response_for_invalid_serializers(*serializers):
    errors = {
        field: error
        for serializer in serializers
        for field, error in serializer.errors.items()
    }
    return Response(
        {"status": "failed", "message": str(errors)},
        status=status.HTTP_400_BAD_REQUEST,
    )


class ApiBaseView:
    def _create_response_for_invalid_serializers(self, *serializers):
        errors = {
            field: error
            for serializer in serializers
            for field, error in serializer.errors.items()
        }
        return Response(
            {"status": "failed", "message": str(errors)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _create_response_for_exception(self, exception):
        return Response(
            {"status": "failed", "message": str(exception.message)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _create_response_not_found(self, exception):
        return Response(
            {"status": "failed", "message": str(exception.message)},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def _create_response_for_successful_create_request(message: str, data=None):
        return Response(
            {
                "status": "success",
                "message": f"Successful created {message}",
                "data": data,
            },
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def _create_response_for_successful_request(message: str, data=None):
        return Response(
            {
                "status": "success",
                "message": f"Successful {message}",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
