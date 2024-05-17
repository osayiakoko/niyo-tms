from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import user_agents


def root_redirect(request):
    user_agent_string = request.META.get("HTTP_USER_AGENT", "")
    user_agent = user_agents.parse(user_agent_string)

    if user_agent.is_mobile:
        schema_view = "doc:redoc"
    else:
        schema_view = "doc:swagger-ui"

    return redirect(schema_view)


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(_):
    return Response()
