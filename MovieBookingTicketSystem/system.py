import sys

from abc import ABC, abstractmethod

class PRODUCT(ABC):

    @abstractmethod
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @abstractmethod
    def purchase_product(self):
        pass

    @abstractmethod
    def cancel_purchase(self):
        pass

    @abstractmethod
    def promotion(self):
        pass

class USER:
    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.__password = password
        self.booking_history = []

    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, new_password):
        if not isinstance(new_password, str) or len(new_password) < 5:
            print("The password must be a string and have at least 5 characters.")
        else:
            self.__password = new_password
    
    def add_booking(self, movie_name):
        self.booking_history.append(movie_name)

    def view_booking_history(self):
        if not self.booking_history:
            print("No past bookings.")
        else:
            print("Past bookings:")
            for ticket in self.booking_history:
                print(f"- {ticket.name} for the movie '{ticket.showtime.movie.name}'")

    
class POPCORN(PRODUCT):
    def __init__(self, name, price, size):
        super().__init__(name, price)
        self.size = size
    
    def purchase_product(self):
        if self.size == "L":
            self.price = 7.5
            self.name = "Pipoca Grande"
        elif self.size == "M":
            self.price = 6.0
            self.name = "Pipoca Média"
        else:
            self.price = 4.5
            self.name = "Pipoca Pequena"
        return self.price
    
    def cancel_purchase(self):
        print(f"Popcorn of size {self.size} purchase cancelled.")    

    def promotion(self):
        if self.size == "L":
            self.price *= 0.9
        elif self.size == "M":
            self.price *= 0.95 
        else:
            self.price = self.price
        return self.price

        
class TICKET(PRODUCT):
    def __init__(self, name, price, seat, showtime):
        super().__init__(name, price)
        self.seat = seat
        self.showtime = showtime
    
    def purchase_product(self):
        if not self.seat.is_reserved:
            self.seat.reserver()
            print(f"Ticket for seat {self.seat.row_and_number} purchased successfully!")
        else:
            print(f"Ticket for seat {self.seat.row_and_number} is already reserved.")
    
    def cancel_purchase(self):
        if self.seat.is_reserved:
            self.seat.release()
            print(f"Ticket for seat {self.seat.row_and_number} cancelled.")
        else:
            print(f"Ticket for seat {self.seat.row_and_number} is not reserved.")

    def promotion(self):
        if self.name in ["Student", "Subscriber"]:
            self.price *= 0.5
        return self.price

class SEAT:
    def __init__(self, row_and_number):
        self.row_and_number = row_and_number
        self.is_reserved = False
    
    def reserver(self):
        if not self.is_reserved:
            self.is_reserved = True
            print(f"Seat {self.row_and_number} reserved successfully!")
        else:
            print(f"Seat {self.row_and_number} is already reserved.")
    
    def release(self):
        if self.is_reserved:
            self.is_reserved = False
            print(f"Seat {self.row_and_number} reservation cancelled.")
        else:
            print(f"Seat {self.row_and_number} is not reserved.")

class SHOWTIME:
    def __init__(self, movie, time, screen_number, seats):
        self.movie = movie
        self.time = time
        self.screen_number = screen_number
        self.seats = seats 

    def list_available_seats(self):
        available_seats = [seat.row_and_number for seat in self.seats if not seat.is_reserved]
        print(f"Assentos disponíveis para '{self.movie.name}' às {self.time}: {', '.join(available_seats)}")
        return available_seats    


class MOVIE:
    def __init__(self, name, duration_in_minutes, genre):
        self.name = name
        self.duration_in_minutes = duration_in_minutes
        self.genre = genre
        self.showtimes = []
        self.reviews = []
    
    def add_showtime(self, time, screen_number, seats):
        new_showtime = SHOWTIME(self, time, screen_number, seats)
        self.showtimes.append(new_showtime)
    
    def list_showtimes(self):
        if not self.showtimes:
            print("No sessions available at {self.name}.")
            return
        
        print(f"Sessions available at {self.name}:")
        for showtime in self.showtimes:
            available_count = len([s for s in showtime.seats if not s.is_reserved])
            print(f"- Horário: {showtime.time} | Sala: {showtime.screen_number} | Assentos disponíveis: {available_count}")        
    
    def add_review(self, rating, comment):
        self.reviews.append({"rating": rating, "comment": comment})

    def get_average_rating(self):
        if not self.reviews:
            return "N/A"
        total_rating = sum(review["rating"] for review in self.reviews)
        return total_rating / len(self.reviews)

class CINEMA:
    def __init__(self, name):
        self.name = name
        self.movies = []
    
    def add_movie(self, movie):
        self.movies.append(movie)
    
    def list_movies(self):
        if not self.movies:
            print("No movies available at this time.")
            return
        
        print(f"Movies available at {self.name}:")  
        for movie in self.movies:
            movie.list_showtimes()
            print("-" * 20)


# --- Funções da Interface de Usuário (CLI) ---
usuarios_registrados = {}
usuario_logado = None
cinemas = {}

def inicializar_dados():
    global cinemas
    cinesystem = CINEMA("Cinesystem")
    filme1_cinesystem = MOVIE("Duna: Parte 2", 166, "Ficção Científica")
    filme2_cinesystem = MOVIE("O Gato de Botas 2", 102, "Animação")
    filme1_cinesystem.add_showtime("19:00", 1, [SEAT(f"A{i}") for i in range(1, 11)])
    filme2_cinesystem.add_showtime("16:00", 2, [SEAT(f"B{i}") for i in range(1, 11)])
    cinesystem.add_movie(filme1_cinesystem)
    cinesystem.add_movie(filme2_cinesystem)

    kinoplex = CINEMA("Kinoplex")
    filme1_kinoplex = MOVIE("Vingadores: Ultimato", 181, "Ação")
    filme2_kinoplex = MOVIE("O Gato de Botas 2", 102, "Animação")
    filme1_kinoplex.add_showtime("20:00", 3, [SEAT(f"C{i}") for i in range(1, 11)])
    filme2_kinoplex.add_showtime("17:00", 4, [SEAT(f"D{i}") for i in range(1, 11)])
    kinoplex.add_movie(filme1_kinoplex)
    kinoplex.add_movie(filme2_kinoplex)
    
    centerplex = CINEMA("Centerplex")
    filme1_centerplex = MOVIE("Duna: Parte 2", 166, "Ficção Científica")
    filme1_centerplex.add_showtime("21:00", 5, [SEAT(f"E{i}") for i in range(1, 11)])
    centerplex.add_movie(filme1_centerplex)

    cinemas["Cinesystem"] = cinesystem
    cinemas["Kinoplex"] = kinoplex
    cinemas["Centerplex"] = centerplex
    
    usuarios_registrados["marcela"] = USER("Marcela", "marcela", "12345")

def menu_principal():
    global usuario_logado
    while True:
        print("\n--- Menu Principal ---")
        if usuario_logado:
            print(f"Bem-vindo(a), {usuario_logado.name}!")
            print("1. Ver Filmes")
            print("2. Minhas Reservas")
            print("3. Avaliar um Filme")
            print("4. Sair (logout)")
        else:
            print("1. Login")
            print("2. Ver Filmes")
            print("3. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            if usuario_logado:
                ver_cinemas()
            else:
                login()
        elif escolha == "2":
            if usuario_logado:
                usuario_logado.view_booking_history()
            else:
                ver_cinemas()
        elif escolha == "3":
            if usuario_logado:
                avaliar_filme()
            else:
                print("Obrigado por usar o sistema! 😊")
                sys.exit()
        elif escolha == "4":
            if usuario_logado:
                usuario_logado = None
                print("Você saiu da sua conta.")
            else:
                print("Opção inválida. Tente novamente.")
        else:
            print("Opção inválida. Tente novamente.")

def login():
    global usuario_logado
    resposta = input("Você já possui cadastro? (sim/não): ").lower()
    
    if resposta == "sim":
        processar_login()
    elif resposta == "nao" or resposta == "não":
        registrar()
    else:
        print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")

def processar_login():
    global usuario_logado
    login_user = input("Login: ")
    password_user = input("Senha: ")
    
    if login_user in usuarios_registrados and usuarios_registrados[login_user].password == password_user:
        usuario_logado = usuarios_registrados[login_user]
        print(f"Login realizado com sucesso! Bem-vindo(a), {usuario_logado.name}.")
    else:
        print("Login ou senha incorretos.")

def registrar():
    name = input("Nome: ")
    login_user = input("Login: ")
    password_user = input("Senha: ")
    
    if login_user in usuarios_registrados:
        print("Esse login já existe. Tente outro.")
    else:
        usuarios_registrados[login_user] = USER(name, login_user, password_user)
        print("Usuário registrado com sucesso!")

def ver_cinemas():
    print("\n--- Escolha um Cinema ---")
    for i, cinema_nome in enumerate(cinemas.keys(), 1):
        print(f"{i}. {cinema_nome}")
    print("0. Voltar ao menu principal")
    
    while True:
        escolha = input("Digite o número do cinema: ")
        if escolha == '0':
            return
        try:
            cinema_nome = list(cinemas.keys())[int(escolha) - 1]
            ver_filmes(cinemas[cinema_nome])
            break
        except (ValueError, IndexError):
            print("Opção inválida.")
            
def ver_filmes(cinema_obj):
    cinema_obj.list_movies()
        
    if not usuario_logado:
        input("Pressione Enter para voltar ao menu...")
        return
        
    escolha_filme = input("Digite o nome do filme que deseja comprar ingresso (ou 'sair' para voltar): ")
    if escolha_filme.lower() == 'sair':
        return
    
    filme_selecionado = next((m for m in cinema_obj.movies if m.name.lower() == escolha_filme.lower()), None)
    if not filme_selecionado:
        print("Filme não encontrado. Tente novamente.")
        return
        
    comprar_ingresso(filme_selecionado)

def comprar_ingresso(movie):
    print(f"\n--- Comprar Ingresso para '{movie.name}' ---")
    movie.list_showtimes()
    
    escolha_horario = input("Digite o horário da sessão (ex: 19:00): ")
    showtime_selecionado = next((s for s in movie.showtimes if s.time == escolha_horario), None)
    
    if not showtime_selecionado:
        print("Horário inválido. Tente novamente.")
        return
        
    print(f"\nHorário selecionado: {showtime_selecionado.time} | Sala: {showtime_selecionado.screen_number}")
    showtime_selecionado.list_available_seats()
    
    escolha_assento = input("Digite o número do assento desejado (ex: A5): ")
    assento_selecionado = next((s for s in showtime_selecionado.seats if s.row_and_number.lower() == escolha_assento.lower()), None)
    
    if not assento_selecionado or assento_selecionado.is_reserved:
        print("Assento inválido ou já reservado.")
        return
    
    tipo_ingresso = input("Digite o tipo de ingresso (Padrão, Estudante, Assinante): ")
    preco = 25.0
    
    ticket = TICKET(f"Ingresso {tipo_ingresso}", preco, assento_selecionado, showtime_selecionado)
    ticket.promotion() #polimorfismo

    print(f"\nResumo da Compra:")
    print(f"Filme: {movie.name}")
    print(f"Sessão: {showtime_selecionado.time} - Sala {showtime_selecionado.screen_number}")
    print(f"Assento: {assento_selecionado.row_and_number}")
    print(f"Preço: R$ {ticket.price:.2f}")

    escolha_combo = input("Deseja adicionar um combo de pipoca? (S/N): ")
    if escolha_combo.lower() == "s":
        combo_size = input("Tamanho da pipoca (P, M, L): ").upper()
        popcorn = POPCORN("Pipoca", 0.0, combo_size)
        popcorn.purchase_product()
        print(f"Combo de {popcorn.name} ({popcorn.size}) adicionado. Preço: R$ {popcorn.price:.2f}")
        ticket.price += popcorn.price

    pagar = input(f"Preço total: R$ {ticket.price:.2f}. Deseja prosseguir com o pagamento? (S/N): ")
    if pagar.lower() == "s":
        ticket.purchase_product()
        usuario_logado.add_booking(ticket)
        print("\nPagamento processado e reserva confirmada! 🥳")
    else:
        print("Compra cancelada.")

def avaliar_filme():
    if not usuario_logado:
        print("Você precisa estar logado para avaliar um filme.")
        return
    
    print("\n--- Escolha um Cinema para Avaliar um Filme ---")
    for i, cinema_nome in enumerate(cinemas.keys(), 1):
        print(f"{i}. {cinema_nome}")
    print("0. Voltar ao menu principal")

    while True:
        escolha = input("Digite o número do cinema: ")
        if escolha == '0':
            return
        try:
            cinema_nome = list(cinemas.keys())[int(escolha) - 1]
            cinema_obj = cinemas[cinema_nome]
            
            print(f"\n--- Filmes disponíveis no {cinema_obj.name} ---")
            for i, movie in enumerate(cinema_obj.movies, 1):
                print(f"{i}. {movie.name}")
            
            escolha_filme = input("Digite o número do filme que deseja avaliar: ")
            movie_to_review = cinema_obj.movies[int(escolha_filme) - 1]

            rating = int(input("Sua avaliação (1 a 5): "))
            if rating < 1 or rating > 5:
                raise ValueError
            comment = input("Seu comentário: ")
            
            movie_to_review.add_review(rating, comment)
            print("Avaliação enviada com sucesso! ✨")
            return

        except (ValueError, IndexError):
            print("Opção inválida. Tente novamente.")

# --- Iniciar o programa ---
if __name__ == "__main__":
    inicializar_dados()
    menu_principal()