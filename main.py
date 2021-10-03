import os,requests
from requests.utils import requote_uri

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files_list(self, ya_cloud_url='https://cloud-api.yandex.net/v1/disk/resources/files/'):
        headers = self.get_headers()
        response = requests.get(url=ya_cloud_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f'Ошибка, код ответа: {response.status_code}'

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(url=upload_url, headers=headers, params=params)

        # тут проверяем, есть ли директория в облачном хранилище
        if response.status_code == 200:
            return response.json()
        else:
            return False

    def upload(self, file_path: str='', hard_disk_dir='files'):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        os_separator = os.path.sep
        path_to_file = hard_disk_dir + os_separator
    
        # получаем все файлы из директории {hard_disk_dir} и записываем в список
        with os.scandir(path_to_file) as file_list:
             
            for file_ in file_list:
                if file_.is_file():
                    response = self._get_upload_link(file_path + file_.name)
                
                    if response:
                        url = response['href']
                        response = requests.put(url=url, data=open(path_to_file + file_.name, 'rb'))
                        response.raise_for_status()
                        if response.status_code == 201:
                            if file_path:
                                print(f'Файл {file_.name} успешно загружен в {file_path}')
                            else:
                                print(f'Файл {file_.name} успешно загружен в корневую папку диска')
                    else:
                        print(f'Ошибка: директории {file_path} нет в облачном хранилище.\nУкажите существующую директорию или оставьте поле пустым для загрузки в корень хранилища')
                        break



if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    token = ...
    uploader = YaUploader(token)
    result = uploader.upload()
