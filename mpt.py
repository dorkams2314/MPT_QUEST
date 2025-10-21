from typing import Dict, List, Set, Tuple, sys

class GameState:
	"""
	ЧЕСТНО!!! написал бы игру на pygame или даже на renPy, НО из-за того, что я не один человек в команде, приходится делать так. УВЫ
	"""
	def __init__(self):
		self.level: int = 1
		self.inventory: List[str] = []
		self.found_items: Set[str] = set()
		self.opened_doors: Set[str] = set()
		self.flags: Dict[str, bool] = {}
		self.coords: Dict[str, Tuple[int, int]] = {
			"дверь_аудитория": (0, 1),
			"компьютер_лаборатория": (2, 3),
			"сцена_актовый_зал": (5, 1)
		}

	def has(self, item: str) -> bool:
		return item in self.inventory

	def add_item(self, item: str):
		if item not in self.inventory:
			self.inventory.append(item)
		self.found_items.add(item)

	def remove_item(self, item: str):
		if item in self.inventory:
			self.inventory.remove(item)

def normalize(text: str) -> str:
	return text.strip().lower()

def parse_command(raw: str) -> Tuple[str, str]:
	raw = normalize(raw)
	if not raw:
		return ("", "")
	parts = raw.split(maxsplit=1)
	verb = parts[0]
	obj = parts[1] if len(parts) > 1 else ""
	return (verb, obj)

def print_help():
	print("""
команды:
	осмотреться           	- описание локации
	взять <предмет>       	- добавить предмет в инвентарь
	использовать <предмет>	- использовать предмет
	инвентарь             	- показать, что есть в инвентаре
	перейти               	- перейти дальше (естевственно когда можно)
	помощь                	- показать эту менюшку
	выход                 	- завершить игру

кстати! попробуй 'осмотреться' на каждом уровне. (я этого не говорил)
	""")

def print_unknown_command():
	print("неизвестная команда. попробуй 'помощь'.")

def exit_game(verb):
	if verb in ("выход", "quit", "exit"):
		print("пока!")
		sys.exit(0)

def show_inventory(state: GameState):
	if state.inventory:
		print("инвентарь:", ", ".join(state.inventory))
	else:
		print("инвентарь пуст.")

def level_1(state: GameState) -> bool:
	print("\n>>>> УРОВЕНЬ 1: аудитория")
	print("ты очухался в пустой аудитории, а на столе — бардак.")
	print("где-то должен быть твой пропуск и ключ от двери в коридор...")
	door_name = "дверь_аудитория"

	items_here: List[str] = ["пропуск", "ключ от двери", "расписание", "флешка"]
	item_desc: Dict[str, str] = {
		"пропуск": "(стандартный студентческий пропуск)",
		"ключ от двери": "(подходят к двери аудитории)",
		"расписание": "(листок с парой заметок и какими-то номерами кабинетов)",
		"флешка": "(на 8 гигабайт. могут быть файлы... а может и вирусняк. кто знает?)"
	}

	door_open = door_name in state.opened_doors

	# ! МНЕ лень это всё выводить в отдельную функцию
	while True:
		cmd = input("> ").strip()
		verb, obj = parse_command(cmd)

		exit_game(verb)

		if verb in ("помощь", "help"):
			print_help()
			continue

		if verb in ("инвентарь",):
			show_inventory(state)
			continue

		if verb in ("осмотреться", "осмотришься", "осмотреть"):
			print("ты видишь стол, стулья и дверь в коридор.")
			print("на столе можно найти:", ", ".join(items_here))
			door_pos = state.coords["дверь_аудитория"]
			print(f"дверь в коридор находится по координатам {door_pos}.")
			continue

		if verb == "взять":
			if not obj:
				print("а че взять? к примеру: 'взять пропуск'")
				continue
			if obj in items_here:
				state.add_item(obj)
				items_here.remove(obj)
				print(f"ты взял: {obj}. {item_desc.get(obj, '')}")
			else:
				print("такого тут нет.")
			continue

		if verb == "использовать":
			if obj == "ключ от двери" and state.has("ключ от двери"):
				state.opened_doors.add(door_name)
				door_open = True
				print("ты открыл дверь аудитории. можно выходить в коридор!")
			elif obj == "пропуск" and state.has("пропуск"):
				print("ты прокрутил в руках пропуск. будет нужен.")
			elif obj == "флешка" and state.has("флешка"):
				print("флешка без компа не поможет. мб, в лаборатории найдётся ПК.")
			else:
				print("не получается использовать это сейчас.")
			continue

		if verb == "перейти":
			if door_open and state.has("пропуск"):
				print("ты выходишь в коридор и направляешься к лаборатории.")
				state.level = 2
				return True
			elif not door_open:
				print("дверь закрыта. нужен ключ.")
			elif not state.has("пропуск"):
				print("без пропуска дальше нельзя, охрана спросит по любому.")
			continue

		print_unknown_command()

def level_2(state: GameState) -> bool:
	print("\n>>>> УРОВЕНЬ 2: лаборатория")
	print("ты входишь в лабораторию. на столе куча деталей и системный блок.")
	print("нужно собрать ПК, чтобы узнать, где проходит последний звонок.")

	all_parts: List[str] = ["плата", "кабель", "блок питания", "кулер", "наклейки", "дискетта"]
	required: Set[str] = {"плата", "кабель", "блок питания"}
	collected: Set[str] = set()
	computer_on = state.flags.get("computer_on", False)
	door_password = "МПТ-2025"
	lab_door_name = "дверь_к_актовому"

	# ! МНЕ лень это всё выводить в отдельную функцию
	while True:
		cmd = input("> ").strip()
		verb, obj = parse_command(cmd)

		exit_game(verb)

		if verb in ("помощь", "help"):
			print_help()
			continue

		if verb in ("инвентарь",):
			show_inventory(state)
			continue

		if verb in ("осмотреться",):
			comp_pos = state.coords["компьютер_лаборатория"]
			print("на столе лежат детали:", ", ".join(all_parts))
			print(f"ПК стоит по координатам {comp_pos}. Он пока выключен." if not computer_on else
					f"ПК по координатам {comp_pos} включён и показывает окно с паролем двери.")
			if collected:
				print("собранные детали:", ", ".join(sorted(collected)))
			continue

		if verb == "взять":
			if not obj:
				print("че взять? к примеру: 'взять плата'")
				continue
			if obj in all_parts:
				state.add_item(obj)
				all_parts.remove(obj)
				print(f"Вы взяли: {obj}.")
			else:
				print("такой детали здесь нет.")
			continue

		if verb == "использовать":
			if obj in ("плата", "кабель", "блок питания"):
				if state.has(obj):
					collected.add(obj)
					print(f"вы установили: {obj}. прогресс сборки: {len(collected)}/{len(required)}.")
				else:
					print("сначала нужно взять эту деталь.")
			elif obj == "кулер":
				if state.has("кулер"):
					print("кулер установлен. охлаждение — это хорошо.")
					collected.add("кулер")
				else:
					print("сначала возьми кулер.")
			elif obj == "дискетта":
				if state.has("дискетта"):
					print("на дискетте какие-то драва. мб пригодятся, но сначала нужен базовый запуск.")
				else:
					print("сначала нужно взять дискетту.")
			elif obj == "включить":
				if required.issubset(collected):
					computer_on = True
					state.flags["computer_on"] = True
					print("опаньки!!! а ПК живой! на экране сообщение:")
					print(f"«Линейка проходит в актовом зале. Пароль двери: {door_password}»")
				else:
					missing = required - collected
					print("не хватает деталей для запуска. отсутствуют:", ", ".join(missing))
			elif obj == "дверь":
				if state.flags.get("computer_on"):
					print("дверь заперта. на панели ввода мигают цифры и буквы.")
					print("пробуй: 'использовать пароль'")
				else:
					print("без инфы с ПК ты не знаешь пароль.")
			elif obj == "пароль":
				if state.flags.get("computer_on"):
					state.opened_doors.add(lab_door_name)
					print("ты ввёл пароль. Дверь в сторону актового зала открыта!")
				else:
					print("ты не знаешь пароль. сначала включи ПК.")
			else:
				print("не получается использовать это сейчас.")
			continue

		if verb == "перейти":
			if lab_door_name in state.opened_doors:
				print("ты выходите из лаборатории и направляетесь в актовый зал.")
				state.level = 3
				return True
			else:
				print("дверь ещё закрыта. нужен пароль.")
			continue

		print_unknown_command()

def level_3(state: GameState) -> bool:
	print("\n>>>> УРОВЕНЬ 3: актовый зал")
	print("ты подходишь ко входу в актовый зал. Завуч строго смотрит на тебя.\n")
	print("— Пропуск покажите. И на вопрос ответьте — тогда и проходите.\n")

	if not state.has("пропуск"):
		print("но увы! без пропуска тебя не впускают. ну похоже, где-то ты его потерял.")
		print("бегом назад и найди его! (перезапусти игру)")
		return False

	stage_pos = state.coords["сцена_актовый_зал"]
	print(f"сцена виднеется вдали, примерно по координатам {stage_pos}.\n")

	riddles: Dict[str, str] = {
		"Без чего прибор не соберёшь: знаний много — толку ноль?": "инструкция",
		"Он память хранит, но не человек. Что это?": "накопитель",
		"То густеет — то редеет, студентов всех бодрит и греет.": "чай"
	}

	question, answer = next(iter(riddles.items()))
	print(f"Завуч: «{question}»")

	attempts = 3
	while attempts > 0:
		user = normalize(input("твой ответ: "))
		if user == normalize(answer):
			print("Завуч кивает: «Верно. Проходи. И не опаздывай больше!»\n") # ну блабалабла
			print("ты успел на последний звонок! игра пройдена йоу.")
			return True
		else:
			attempts -= 1
			if attempts:
				print(f"неправильно. осталось попыток: {attempts}. подумай ещё.")
			else:
				print("доигрался... до следующего раза")
				return False
		print("\nспасибо за игру легенда!!")

def greet() -> str:
	print("«Последний звонок: квест по МПТ»")
	name = input("как звать? (опционально): ").strip()
	allowedName = "данёк"

	tempWord = "не опоздывай"
	if name != allowedName:
		print(f"дароу, {name}! {tempWord}")
	elif name == allowedName:
		print(f"ОГО КАКИЕ ЛЮДИ, давай {tempWord}")
	else:
		print(f"дароу! {tempWord}")

	print("используй 'помощь', чтобы увидеть команды.")

	return name

def main():
	state = GameState()
	greet()

	if not level_1(state):
		return
	if not level_2(state):
		return
	level_3(state)

main() # ОПАНА
