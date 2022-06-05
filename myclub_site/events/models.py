# \myclub_root\events\models.py

from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model): # вся инфа о пользователях. в частности, их telegram_id - самое важное.
    username = models.CharField('User Nik', default='Some User', max_length=30, help_text="Никнейм (необязателен)")
    userIsEng = models.BooleanField('Is English',default=False, help_text="По умолчанию, общение на русском; Если тут True, - с ним будут общаться на английском.")
    email = models.EmailField('User Email', null=True, help_text="Email (необязательно)")
    telegram_id = models.BigIntegerField(null=False, unique=True, help_text="Это только лишь цифры! Это бот/скрипт получает, - пока неизвестно, где технически раздобыть эти цифры можно..")
    has_payed = models.BooleanField(default=False, help_text="Уже платил или нет - типа, пользователь с привилегиями или нет")
    num_files_downloaded = models.PositiveIntegerField(default=0, help_text="Сколько файлов скачал накачал / запросил")
    gb_downloaded = models.PositiveIntegerField(default=0, help_text="Сколько ГИГАбайт скачал.. - можно легко вычислить теперь лимитчиков")
    mb_downloaded = models.PositiveIntegerField(default=0, help_text="Сколько МЕГАбайт скачал.. - можно легко вычислить теперь лимитчиков")
    gb_has_now = models.PositiveIntegerField(default=0, help_text="К-во гигабайт, которым обладает сейчас")
    is_limited = models.BooleanField(default=False, help_text="Ограничен ли в правах на кач")
    max_connections_limit = models.PositiveIntegerField(default=5, help_text="К-во макс. одновременных скачек")
    max_gb_can_download = models.PositiveIntegerField(default=100, help_text="К-во гигабайт, разрешённое к скачке")
    max_gb_can_have = models.PositiveIntegerField(default=50, help_text="К-во гигабайт, которое может хранить (размер персонального хранилища)")
    when_started = models.DateTimeField(auto_now_add=True, help_text="Когда начал качать, - полезно для оживления / удаления / чистки мертвецов")
    when_last_activity = models.DateTimeField(auto_now=True, help_text="Когда последняя активность / запрос на существующий видос.. полезно для чистки / оживления / удаления.. мертвечины...")
    when_last_download = models.DateTimeField(null=True, help_text="Когда последняя скачка.. полезно для чистки / оживления / удаления спящих...")
    downloading_now = models.PositiveIntegerField(default=0, help_text="Сколько сейчас качает он потоков")
    waiting_channels_now = models.PositiveIntegerField(default=0, help_text="Сколько сейчас ждёт каналов он")
    invited_people = models.PositiveIntegerField(default=0, help_text="Сколько пользователей он притащил")
    personal_invite_token = models.PositiveIntegerField(default=0, help_text="Токен на приглос")
    tariff = models.PositiveIntegerField(default=0, help_text="Номер тарифного плана...")
    payed_untill = models.DateTimeField(auto_now_add=True, help_text="До какого числа тариф оплачен")
    is_premium = models.BooleanField(default=False, help_text="Премиум-пользователь")
    userLog = models.TextField(null=True, help_text='активность пользователя.. последние XX записей..') # к-во записей определяется в botwork в классе, там.. при создании.
    def __str__(self):
        return str(self.telegram_id)

class MySessions(models.Model): # вся инфа о сессиях. в частности, кто начал сессию, и зачем, и когда началась.
    who_started = models.BigIntegerField(null=False, help_text="TELEGRAM ID пользователя, стартовавшего сессию..")
    when_started = models.DateTimeField(auto_now_add=True, help_text="Когда начал сессию?..")
    why_started = models.CharField(default='Some UNKNOWN session..', max_length=2048, help_text='Причина начала сессии...')
    session_id = models.BigIntegerField(null=False, help_text="уникальный ID сессии..")
    def __str__(self):
        return str(self.session_id)

class MyVidPatterns(models.Model): # ВНИМАНИЕ!!! только лишь пока на youtube всё работает. других КАНАЛОВ особенно, и ИМЁН файлов, неизвестно пока как получать, см. botwork
    # if link is, like, https://m.youtube.com/channel/s0meSH1t, then video id is s0meSH1t and starts at 30. and is CHANNEL/STREAM.
    # probably wrong idea to put and store it like that, but i prefer it to be STRICTLY as it is. USER-DEFINED by admin.
    # for, you see, it may even not start with https://, it may be just http://, or just m.youtu.be/watch/shit, or www.youtube.com, or youtube.com/shit, or it may be not even youtube.!!
    vid_url_sub = models.CharField(default='s://youtube.com/watch', max_length=1024, help_text='паттерн: подстрока из URL - типа, s://youtube.com/watch')
    id_starts_at = models.PositiveIntegerField(default=28, help_text='откуда (с какого символа) стартует КОД (ID) - канала или видео')
    vid_url_prefix = models.CharField(default='https://youtube.com/watch?v=', max_length=1024, help_text='- вида https://youtube.com/watch?v=, т.е. куда (на какой URL) бьёт паттерн.. необязательное поле, но если указать напрямую здесь, будет лучше. чем вычислять. - тем более, могут поменять это в любой момент то...') # for the channel, it links to channel's feed.xml only.. 
    vid_provider_name = models.CharField(default='YouTube', max_length=1024, help_text='youtube / rutube / ещё какаянить хуйня.. по идее, ytdlp может качать и не только с youtube.')
    vid_is_channel = models.BooleanField(default=False, help_text='если это - канал, то ID видоса может быть только лишь получен из .XML-фида канала. (тогда, когда он там появится.)') # we then await for feed.xml to change and give us a link.
    def __str__(self):
        return self.vid_url_sub + ":" + str(self.id_starts_at)
    def link_prefix(self):
        return self.vid_url_prefix

class Vidos(models.Model): # вся инфа о видосах. в частности, кто из пользователей запросил (самое важное), и кто скачал, и где хранится, итд.
    name = models.CharField(default='Some UnDownloaded Video..', max_length=1024, help_text='Имя видео. НЕ имя файла.')
    folder = models.CharField(max_length=500,default='/mnt/aud', help_text='где в какой папке лежит находится... по идее, надобно раскидывать видосы по папкам пользователей, чтоб система не охуела там.')
    filename = models.CharField(default='Some_FileName', max_length=2000, help_text='тут предполагается имя файла') # possibly, later should be changed to FileField...
    video_id = models.CharField(max_length=260, null=False, help_text='YOUTUBE-id скачанного видео')
    bot_video_id = models.CharField(max_length=300, default='UNDEF', help_text='TELEGRAM-id отправленного видео')
    is_stream = models.BooleanField(default=False, help_text='стрим ли это был')
    is_awaited = models.BooleanField(default=True, help_text='если ещё ждём его') # possibly needs split, Vidos/Channel... later on, i thinks..
    is_part = models.PositiveIntegerField(default=0, help_text='если это часть стрима какая-то, - то какая по счёту')
    of_parts = models.PositiveIntegerField(default=0, help_text='из скольких частей стрим состоит')
    is_downloaded = models.BooleanField(default=False, help_text='уже скачано или ещё ожидается / качается')
    is_broken = models.BooleanField(default=False, help_text='докачано нормально, или жёваное')
    is_for_money = models.BooleanField(default=False, help_text='за деньги продаётся, или так..')
    is_payed = models.BooleanField(default=False, help_text='оплачено уже, или нет')
    price_for_all_rub = models.DecimalField(default=50, max_digits=5, decimal_places=2, blank=True, help_text='цена для всех общая (в рублях)')
    description = models.TextField(null=True, help_text='описание видео; тут по идее както нужно вытаскивать сюда его откудато.')
    weight_mb = models.PositiveIntegerField(default=1, help_text='вес в мегабайтах')
    is_heavy=models.BooleanField(default=False, help_text='признак: тяжёлое или нет. - чтобы проще было потом отсеивать/чистить говно')
    time_to_download_sec = models.PositiveIntegerField(default=0, help_text='сколько времени потребовалось на скачку')
    when_started = models.DateTimeField(auto_now_add=True, help_text='когда начата скачка, - дата, время')
    when_downloaded = models.DateTimeField(auto_now=True, help_text='когда окончена скачка. - дата, время. вроде как не должно меняться при обновлении...')
    when_requested = models.DateTimeField(auto_now=True, help_text='когда запрошено... вроде как, - ДОЛЖНО меняться при обновлении...')
    times_requested = models.PositiveIntegerField(default=0, help_text='сколько раз запрошено')
    he_downloaded = models.BigIntegerField(null=False, help_text='Telegram ID того, кто скачал видос. Может и быть пустым, если удалят удалим пользователя..')
    vidLink = models.URLField(null=True, help_text='url видоса...')
    vidProvider = models.CharField(max_length=25, default='YouTube', help_text='сервис-провайдер видоса..')
    vidLog = models.TextField(null=True, blank=True, help_text='активность по видосу.. последние XX записей..') # к-во записей определяется в vidwork в классе, там.. при создании.
    # MAIN MANY-TO-MANY DATA IS:
    they_requested_download = models.ManyToManyField(MyUser, blank=True, help_text='Кто ещё запросил скачку такого же видео. ИМЕННО ЭТО ПОЛЕ - РЕАЛИЗУЕТ МОДЕЛЬ MANY-TO-MANY. без него и база-то не нужна...') 
    is_from_channel = models.CharField(max_length=300, default='NONE', help_text='YOUTUBE-id канала, с которого скачано видео')
    def __str__(self):
        return str(self.video_id) + " " + self.name + " " + self.filename

class Chan(models.Model): # вся инфа о КАНАЛАХ. в частности, кто из пользователей на какой канал ПОДПИСАН, - чтобы высылать пользователю/лям новые видео с канала
    channel_id = models.CharField(max_length=300, null=False, help_text='YOUTUBE-id канала')
    he_started = models.BigIntegerField(null=False, help_text='Telegram ID того, кто первым подписан..')
    is_for_money = models.BooleanField(default=False, help_text='за деньги продаётся, или так..')
    is_payed = models.BooleanField(default=False, help_text='оплачено уже, или нет')
    price_for_all_rub = models.DecimalField(default=50, max_digits=5, decimal_places=2, blank=True, help_text='цена для всех общая (в рублях)')
    name = models.CharField(default='Some Unknown Channel..', max_length=1024, help_text='Название канала. Для простоты понимания.') 
    they_requested_chan = models.ManyToManyField(MyUser, blank=True, help_text='Кто подписан на канал...') 
    when_started = models.DateTimeField(auto_now_add=True, help_text='когда начата прослушка, - дата, время')
    when_last_vid = models.DateTimeField(auto_now=True, help_text='когда последняя скачка. - дата, время.')
    last_vid = models.CharField(max_length=260, default='none', help_text='YOUTUBE-id последнего видео')
    hours_to_refresh = models.PositiveIntegerField(default=0, help_text='раз во сколько часов в среднем обновляется...')
    avg_video_weight = models.PositiveIntegerField(default=0, help_text='вес среднего видео')
    def __str__(self):
        return self.name

class Mess(models.Model): # сообщения от пользователей - результаты диалогов:
    he_sent = models.ForeignKey(MyUser, null=True, help_text='Кто отправил сообщение...', on_delete=models.SET_NULL)
    description = models.TextField(null=True, help_text='Чего отправил в сообщении..')
    when_started = models.DateTimeField(auto_now_add=True, help_text='Когда отправил сообщение.')

class ST(models.Model): # статистика по системе...
    date = models.DateTimeField(null=True, help_text='день сбора статистики')
    num_new_users = models.BigIntegerField(default=0, help_text='к-во новых пользователей..')
    active_users = models.ManyToManyField(MyUser, blank=True, help_text='активны за этот день...')
    num_files_requested = models.BigIntegerField(default=0, help_text='к-во файлов запрошено..')
    num_files_downloaded = models.BigIntegerField(default=0, help_text='к-во файлов загружено..')
    gb_downloaded = models.BigIntegerField(default=0, help_text='к-во GB загружено..')
    gb_stored = models.BigIntegerField(default=0, help_text='сколько GB в хранилище..')
    files_stored = models.BigIntegerField(default=0, help_text='сколько файлов в хранилище..')

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip/Post Code', max_length=12)
    phone = models.CharField('Contact Phone', max_length=20, blank=True)
    web = models.URLField('Web Address')
    email_address = models.EmailField('Email Address')
    def __str__(self):
       return self.name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    attendees = models.ManyToManyField(MyUser, blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
