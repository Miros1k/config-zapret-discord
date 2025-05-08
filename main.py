import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import sys
import tempfile
import webbrowser

if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

class BatLauncher:
      def __init__(self, root):
          self.root = root
          self.root.title("Запуск BAT файлов")
          self.root.geometry("600x700")
        
          # Стиль
          style = ttk.Style()
          style.theme_use('clam')
        
          # Основная рамка
          self.main_frame = ttk.Frame(root, padding="10")
          self.main_frame.pack(fill=tk.BOTH, expand=True)
        
          # Заголовок
          title_label = ttk.Label(self.main_frame, text="Управление BAT файлами",
                                font=('Arial', 14, 'bold'))
          title_label.pack(pady=10)

          # Секции
          self.sections = {
              "Основные файлы (Обход блокировок Discord и YouTube)": ["general.bat", "discord.bat","general (ALT).bat","general (ALT2).bat","general (ALT3).bat","general (ALT4).bat","general (ALT5).bat","general (FAKE TLS MOD ALT).bat","general (FAKE TLS MOD).bat","general (МГТС).bat","general (МГТС2).bat"],
              "Управление сервисом (Установка/удаление/диагностика)": ["service_remove.bat", "service_install.bat","service_status.bat"],
              "Дополнительные (Управление Cloudflare и обновления)": ["cloudflare_switch.bat","check_updates.bat"],
              "Антивирус и безопасность": None, 
              "Решение проблем": None,
              "Автор zapret-discord и сылка на сайт": None
          }

          # Создаем фреймы для каждой секции
          self.section_frames = {}
          self.section_buttons = {}
          self.section_listboxes = {}
          self.section_descriptions = {
              "Основные файлы (Обход блокировок Discord и YouTube)": "Файлы для обхода блокировок Discord и YouTube с разными стратегиями",
              "Управление сервисом (Установка/удаление/диагностика)": "Инструменты для управления службой zapret",
              "Дополнительные (Управление Cloudflare и обновления)": "Дополнительные утилиты для работы с Cloudflare и обновлениями",
              "Антивирус и безопасность": "WinDivert может вызвать реакцию антивируса. WinDivert - это инструмент для перехвата и фильтрации трафика, необходимый для работы zapret. Замена iptables и NFQUEUE в Linux, которых нет под Windows. Он может использоваться как хорошими, так и плохими программами, но сам по себе не является вирусом. Драйвер WinDivert64.sys подписан для возможности загрузки в 64-битное ядро Windows. Но антивирусы склонны относить подобное к классам повышенного риска или хакерским инструментам. В случае проблем используйте исключения или выключайте антивирус совсем.",
              "Решение проблем": "Решения распространенных проблем с Discord, YouTube можно найти на оффициальном сайте zapret",
              "Расширение функционала": "Добавление новых адресов в list-general.txt и list-discord.txt",
              "Автор zapret-discord и сылка на сайт": None
          }
        
          for section_name in self.sections:
              # Создаем кнопку-заголовок секции
              section_button = ttk.Button(
                  self.main_frame,
                  text=section_name,
                  command=lambda s=section_name: self.toggle_section(s)
              )
              section_button.pack(fill=tk.X, padx=5, pady=2)
              self.section_buttons[section_name] = section_button
            
              # Создаем скрываемый фрейм для списка файлов и описания
              section_frame = ttk.LabelFrame(self.main_frame, padding=5)
              section_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
              
              # Специальная обработка для секции с автором
              if section_name == "Автор zapret-discord и сылка на сайт":
                  author_label = ttk.Label(section_frame, text="Автор zapret-discord Flowseal")
                  author_label.pack(fill=tk.X, pady=2)
                  
                  link = ttk.Label(section_frame, text="https://github.com/Flowseal/zapret-discord-youtube",
                                 foreground="blue", cursor="hand2")
                  link.pack(fill=tk.X, pady=2)
                  link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Flowseal/zapret-discord-youtube"))
              else:
                  # Добавляем описание секции
                  description_label = ttk.Label(section_frame, 
                                             text=self.section_descriptions.get(section_name, ""),
                                             wraplength=550)
                  description_label.pack(fill=tk.X, pady=2)
              
              section_frame.pack_forget()  # Скрываем изначально
              self.section_frames[section_name] = section_frame
            
              # Создаем список с прокруткой только для секций с файлами
              if self.sections[section_name] is not None:
                  scrollbar = ttk.Scrollbar(section_frame)
                  scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
                  listbox = tk.Listbox(
                      section_frame,
                      yscrollcommand=scrollbar.set,
                      font=('Arial', 10),
                      selectmode=tk.SINGLE,
                      height=4
                  )
                  listbox.pack(fill=tk.BOTH, expand=True)
                  scrollbar.config(command=listbox.yview)
                  self.section_listboxes[section_name] = listbox

          # Кнопки управления
          button_frame = ttk.Frame(self.main_frame)
          button_frame.pack(fill=tk.X, pady=10)
        
          ttk.Button(button_frame, text="Обновить список",
                    command=self.refresh_files).pack(side=tk.LEFT, padx=5)
          ttk.Button(button_frame, text="Запустить от имени администратора",
                    command=self.run_selected_file).pack(side=tk.LEFT, padx=5)
          ttk.Button(button_frame, text="Выход",
                    command=root.quit).pack(side=tk.RIGHT, padx=5)

          # Информационная панель
          info_frame = ttk.LabelFrame(self.main_frame, text="Информация", padding=5)
          info_frame.pack(fill=tk.X, padx=5, pady=5)
          info_text = "⚠️ Примечание: Для корректной работы требуются права администратора.\nWinDivert может вызвать реакцию антивируса - это нормально, используйте исключения.\nПри проблемах с работой проверьте другие стратегии (ALT/МГТС)."
          ttk.Label(info_frame, text=info_text, wraplength=550).pack(pady=5)

          # Создаем временный bat файл для запуска с правами администратора
          temp_dir = tempfile.gettempdir()
          self.admin_bat_path = os.path.join(temp_dir, "run_admin.bat")
          
          with open(self.admin_bat_path, "w", encoding='utf-8') as f:
              f.write("@echo off\n")
              f.write("chcp 65001>nul\n")
              f.write("set PYTHONIOENCODING=utf-8\n")
              f.write("cls\n")
              f.write("mode con: cols=120 lines=30\n")
              f.write("%*\n")
              f.write("powershell -command \"$wshell = New-Object -ComObject wscript.shell; $wshell.AppActivate('cmd.exe'); Start-Sleep -Milliseconds 500; Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{F11}'); Start-Sleep -Milliseconds 500; $wshell.SendKeys('~')\"\n")
              f.write("echo | set /p='' | %*\n")
              f.write("exit\n")

          # Загружаем файлы при старте
          self.refresh_files()    

      def toggle_section(self, section_name):
          """Переключение видимости секции"""
          if self.section_frames[section_name].winfo_viewable():
              self.section_frames[section_name].pack_forget()
          else:
              # Скрываем все секции
              for frame in self.section_frames.values():
                  frame.pack_forget()
              # Показываем выбранную секцию
              self.section_frames[section_name].pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

      def refresh_files(self):
          """Обновление списка BAT файлов по секциям"""
          try:
              if getattr(sys, 'frozen', False):
                  script_dir = os.path.dirname(sys.executable)
              else:
                  script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
              internal_path = os.path.join(script_dir, '_internal')
              files = [f for f in os.listdir(internal_path) if f.endswith('.bat')]
            
              # Очищаем все списки
              for section_name, listbox in self.section_listboxes.items():
                  listbox.delete(0, tk.END)
            
              # Распределяем файлы по секциям
              for file in sorted(files):
                  added = False
                  for section_name, section_files in self.sections.items():
                      if section_files is not None and file in section_files:
                          self.section_listboxes[section_name].insert(tk.END, file)
                          added = True
                          break
                
                  if not added and "Дополнительные" in self.section_listboxes:
                      # Добавляем неизвестные файлы в "Дополнительные"
                      self.section_listboxes["Дополнительные (Управление Cloudflare и обновления)"].insert(tk.END, file)
                    
          except Exception as e:
              messagebox.showerror("Ошибка", f"Не удалось загрузить список файлов: {str(e)}")

      def run_selected_file(self):
          """Запуск выбранного BAT файла"""
          selected_file = None
          selected_section = None
        
          # Проверяем все секции на выбранный файл
          for section_name, listbox in self.section_listboxes.items():
              if listbox.curselection():
                  selected_file = listbox.get(listbox.curselection()[0])
                  selected_section = section_name
                  break
        
          if not selected_file:
              messagebox.showwarning("Предупреждение", "Выберите файл для запуска")
              return
        
          try:
              if getattr(sys, 'frozen', False):
                  script_dir = os.path.dirname(sys.executable)
              else:
                  script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
              internal_path = os.path.join(script_dir, '_internal')
              bat_path = os.path.join(internal_path, selected_file)
              
              if os.path.exists(bat_path):
                  startupinfo = subprocess.STARTUPINFO()
                  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                  subprocess.Popen([bat_path], shell=True, startupinfo=startupinfo, stdin=subprocess.PIPE)
                  messagebox.showinfo("Успех", f"Файл {selected_file} запущен")
              else:
                  messagebox.showerror("Ошибка", f"Файл {selected_file} не найден")
          except Exception as e:
              messagebox.showerror("Ошибка", f"Не удалось запустить файл: {str(e)}")

      def __del__(self):
          """Деструктор для удаления временного файла"""
          try:
              if hasattr(self, 'admin_bat_path') and os.path.exists(self.admin_bat_path):
                  os.remove(self.admin_bat_path)
          except:
              pass

if __name__ == "__main__":
      root = tk.Tk()
      app = BatLauncher(root)
      root.mainloop()