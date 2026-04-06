# Auth — Полный справочник

> Читать когда: нужны подробности по регистрации, входу, OTP, OAuth, управлению сессией или пользователем.

---

## Регистрация (Sign Up)

```csharp
// Email + пароль
var session = await supabase.Auth.SignUp(email, password);

// Проверка: если подтверждение email включено в Dashboard,
// session будет null до момента подтверждения
if (session?.User != null && session.Session == null)
{
    // Пользователь создан, ждём подтверждения email
}

// С дополнительными метаданными пользователя
var session = await supabase.Auth.SignUp(new SignUpWithPasswordCredentials
{
    Email    = email,
    Password = password,
    Options  = new SignUpWithPasswordCredentials.SignUpOptions
    {
        Data = new Dictionary<string, object>
        {
            { "username", "alice" },
            { "avatar_url", "https://..." }
        }
    }
});
```

**Поведение при `Confirm email` в Dashboard:**

| Настройка | `user` | `session` |
|---|---|---|
| Confirm email **включён** | возвращается | `null` |
| Confirm email **выключен** | возвращается | возвращается |

> Если вызвать SignUp для уже подтверждённого пользователя с включёнными обоими подтверждениями — вернётся обфусцированный/фейковый объект (не ошибка).

---

## Вход по паролю (Sign In)

```csharp
// Email + пароль
var session = await supabase.Auth.SignIn(email, password);
// или
var session = await supabase.Auth.SignInWithPassword(email, password);

// Телефон + пароль
var session = await supabase.Auth.SignIn(SignInType.Phone, phoneNumber, password);
```

---

## Magic Link / OTP по Email

```csharp
// Отправить magic link
await supabase.Auth.SignInWithOtp(
    new SignInWithPasswordlessEmailOptions(email));

// Отправить OTP (6-значный код)
await supabase.Auth.SignInWithOtp(
    new SignInWithPasswordlessEmailOptions(email)
    {
        ShouldCreateUser = false  // не создавать нового пользователя
    });

// Верифицировать OTP-код
var session = await supabase.Auth.VerifyOtp(
    email, token, EmailOtpType.Email);

// OTP по телефону
await supabase.Auth.SignInWithOtp(
    new SignInWithPasswordlessSmsOptions(phoneNumber));

var session = await supabase.Auth.VerifyOtp(
    phone, token, MobileOtpType.SMS);
```

---

## OAuth (сторонние провайдеры)

```csharp
// Получить URL для редиректа пользователя
var signInUrl = await supabase.Auth.SignInWithOAuth(Provider.Google);
// Затем перенаправить пользователя на signInUrl.Uri

// Другие провайдеры:
// Provider.GitHub | Provider.Apple | Provider.Facebook |
// Provider.Discord | Provider.Twitter | Provider.Spotify | и др.

// С redirect URL
var signInUrl = await supabase.Auth.SignInWithOAuth(Provider.GitHub,
    new SignInWithOAuthOptions
    {
        RedirectTo = "myapp://auth/callback"
    });
```

---

## Выход (Sign Out)

```csharp
await supabase.Auth.SignOut();
// Удаляет локальную сессию и инвалидирует токен на сервере
```

---

## Сессия и пользователь

```csharp
// Получить текущую сессию
var session = await supabase.Auth.GetSession();

if (session != null)
{
    var accessToken  = session.AccessToken;
    var refreshToken = session.RefreshToken;
    var expiresAt    = session.ExpiresAt;
}

// Получить данные текущего пользователя (запрос к серверу)
var user = await supabase.Auth.GetUser(session.AccessToken);
Console.WriteLine(user.Email);
Console.WriteLine(user.Id);      // UUID пользователя

// Обновить данные пользователя
await supabase.Auth.UpdateUser(new UserAttributes
{
    Email    = "new@email.com",
    Password = "newpassword123",
    Data     = new Dictionary<string, object>
    {
        { "username", "new_username" }
    }
});
```

---

## Слушатель событий Auth

```csharp
supabase.Auth.AddStateChangedListener((sender, state) =>
{
    switch (state)
    {
        case AuthState.SignedIn:
            Console.WriteLine("Пользователь вошёл");
            break;
        case AuthState.SignedOut:
            Console.WriteLine("Пользователь вышел");
            break;
        case AuthState.TokenRefreshed:
            Console.WriteLine("Токен обновлён");
            break;
        case AuthState.UserUpdated:
            Console.WriteLine("Данные пользователя изменены");
            break;
    }
});
```

---

## Сохранение сессии (MAUI / мобильные платформы)

Реализуйте `ISupabaseSessionHandler` для персистентности токена:

```csharp
public class SupabaseSessionHandler : ISupabaseSessionHandler
{
    public Task<Session?> LoadSession()
    {
        var json = Preferences.Get("supabase_session", null);
        if (json == null) return Task.FromResult<Session?>(null);
        return Task.FromResult(JsonConvert.DeserializeObject<Session>(json));
    }

    public Task SaveSession(Session session)
    {
        Preferences.Set("supabase_session", JsonConvert.SerializeObject(session));
        return Task.CompletedTask;
    }

    public Task DestroySession()
    {
        Preferences.Remove("supabase_session");
        return Task.CompletedTask;
    }
}

// Регистрация в SupabaseOptions:
var options = new SupabaseOptions
{
    AutoRefreshToken = true,
    SessionHandler   = new SupabaseSessionHandler()
};
```

---

## Типичные ошибки Auth

| Ситуация | Проблема | Решение |
|---|---|---|
| `session == null` после SignUp | Включено подтверждение email | Проверяйте `session != null` перед использованием токена |
| `User already registered` | Повторный SignUp без подтверждений | Это ожидаемое поведение — обрабатывайте как ошибку |
| Токен протухает в фоне | `AutoRefreshToken = false` | Установите `AutoRefreshToken = true` |
| Сессия теряется после рестарта | Нет `SessionHandler` | Реализуйте `ISupabaseSessionHandler` |
