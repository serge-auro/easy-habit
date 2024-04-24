
# Документация к методам бота

## Обработчики команд и callback-запросов

### `create_inline_keyboard(button_keys)`
Создает и возвращает объект inline-клавиатуры. 
- **Параметры**:
  - `button_keys` (list): список ключей для кнопок, которые должны быть добавлены в клавиатуру.
- **Возвращает**:
  - `InlineKeyboardMarkup`: объект клавиатуры с заданными кнопками.

### `handle_menu(call)`
Обработчик для возврата пользователя в главное меню.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `handle_status(call)`
Отображает статус текущих привычек пользователя.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `handle_report(call)`
Предоставляет отчет по привычкам пользователя.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `handle_edit_habit(call)`
Позволяет пользователю выбрать привычку для редактирования.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `edit_selected_habit_frequency(call)`
Позволяет пользователю выбрать периодичность для редактируемой привычки.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `request_habit_repetition_input(call)`
Запрашивает у пользователя количество повторений для выбранной привычки.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `handle_repetition_count_input(message)`
Обрабатывает введенное пользователем количество повторений и сохраняет его.
- **Параметры**:
  - `message` (Message): сообщение от пользователя.

### `handle_new_habit(call)`
Обработчик для создания новой привычки.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `handle_del_habit(call)`
Позволяет пользователю выбрать и удалить привычку.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `delete_selected_habit(call)`
Удаляет выбранную привычку.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `handle_mark_habit(call)`
Позволяет пользователю отметить привычку как выполненную.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `mark_selected_habit(call)`
Отмечает выбранную привычку как выполненную.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `handle_habits(call)`
Показывает список всех привычек пользователя.
- **Параметры**:
  - `call` (CallbackQuery): объект callback-запроса от Telegram.

### `handle_start(message)`
Обработчик для команды /start, инициализирует пользователя.
- **Параметры**:
  - `message` (Message): сообщение от пользователя.

### `handle_help(message)`
Обработчик для команды /help, показывает помощь.
- **Параметры**:
  - `message` (Message): сообщение от пользователя.
