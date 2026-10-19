def get_google_access_token(code: str) -> str:
    """Обменивает одноразовый code на access_token от Google."""

    if not all([
        settings.GOOGLE_CLIENT_ID,
        settings.GOOGLE_CLIENT_SECRET,
        settings.GOOGLE_REDIRECT_URI,
    ]):
        raise AuthenticationFailed("Настройки Google OAuth не заполнены.")

    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(token_url, data=data, timeout=10)
    except requests.RequestException as exc:
        print("Google connection error:", str(exc))
        raise AuthenticationFailed(
            "Не удалось подключиться к Google."
        ) from exc

    if not response.ok:
        print("Google status:", response.status_code)
        print("Google response:", response.text)

        raise AuthenticationFailed(
            "Google отклонил запрос. Подробности смотри в терминале."
        )

    try:
        token_data = response.json()
    except ValueError as exc:
        raise AuthenticationFailed(
            "Google вернул некорректный ответ."
        ) from exc

    access_token = token_data.get("access_token")

    if not access_token:
        raise AuthenticationFailed("Google не вернул access_token.")

    return access_token