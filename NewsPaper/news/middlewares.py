#pip install pyyaml ua-parser user-agents

from user_agents import parse


class ViewVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        agent = request.META['HTTP_USER_AGENT']
        user_agent = parse(agent)
        # Мобильный клиент
        user_agent.is_mobile
        # Планшет
        user_agent.is_tablet
        # Поддерживает касания
        user_agent.is_touch_capable
        # ПК
        user_agent.is_pc
        # Поисковый бот
        user_agent.is_bot
        # if user_agent.is_pc:
        #     template_link = "full/"
        # elif user_agent.is_mobile:
        #     template_link = "mobile/"
        #response.template_name = template_link + response.template_name[0]
        return response
        
        # sudo systemctl restart apache2

        # http://192.168.1.101/