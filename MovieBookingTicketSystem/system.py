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
    filme1_cinesystem = MOVIE("Duna: Parte 2", 166, "Sci-Fi")
    filme2_cinesystem = MOVIE("O Gato de Botas 2", 102, "Animation")
    filme1_cinesystem.add_showtime("19:00", 1, [SEAT(f"A{i}") for i in range(1, 11)])
    filme2_cinesystem.add_showtime("16:00", 2, [SEAT(f"B{i}") for i in range(1, 11)])
    cinesystem.add_movie(filme1_cinesystem)
    cinesystem.add_movie(filme2_cinesystem)

    kinoplex = CINEMA("Kinoplex")
    filme1_kinoplex = MOVIE("Vingadores: Ultimato", 181, "Action")
    filme2_kinoplex = MOVIE("O Gato de Botas 2", 102, "Animation")
    filme1_kinoplex.add_showtime("20:00", 3, [SEAT(f"C{i}") for i in range(1, 11)])
    filme2_kinoplex.add_showtime("17:00", 4, [SEAT(f"D{i}") for i in range(1, 11)])
    kinoplex.add_movie(filme1_kinoplex)
    kinoplex.add_movie(filme2_kinoplex)
    
    centerplex = CINEMA("Centerplex")
    filme1_centerplex = MOVIE("Duna: Parte 2", 166, "Sci-Fi")
    filme1_centerplex.add_showtime("21:00", 5, [SEAT(f"E{i}") for i in range(1, 11)])
    centerplex.add_movie(filme1_centerplex)

    cinemas["Cinesystem"] = cinesystem
    cinemas["Kinoplex"] = kinoplex
    cinemas["Centerplex"] = centerplex
    
    usuarios_registrados["marcela"] = USER("Marcela", "marcela", "12345")

def menu_principal():
    global usuario_logado
    while True:
        print("\n--- Main Menu ---")
        if usuario_logado:
            print(f"Welcome, {usuario_logado.name}!")
            print("1. Watch Movies")
            print("2. My Reservations")
            print("3. Reviewing a Movie")
            print("4. Logout")
        else:
            print("1. Login")
            print("2. Watch Movies")
            print("3. Exit")
        
        escolha = input("Select an option: ")

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
                print("Thank you for using the system!")
                sys.exit()
        elif escolha == "4":
            if usuario_logado:
                usuario_logado = None
                print("You have logged out of your account.")
            else:
                print("Invalid option. Please try again.")
        else:
            print("Invalid option. Please try again.")

def login():
    global usuario_logado
    resposta = input("Are you already registered? (yes/no): ").lower()
    
    if resposta == "yes":
        processar_login()
    elif resposta == "no":
        registrar()
    else:
        print("Resposta inválida. Por favor, digite 'yes' ou 'no'.")

def processar_login():
    global usuario_logado
    login_user = input("Login: ")
    password_user = input("Password: ")
    
    if login_user in usuarios_registrados and usuarios_registrados[login_user].password == password_user:
        usuario_logado = usuarios_registrados[login_user]
        print(f"Login successful! Welcome!, {usuario_logado.name}.")
    else:
        print("Incorrect login or password.")

def registrar():
    name = input("Name: ")
    login_user = input("Login: ")
    password_user = input("Password: ")
    
    if login_user in usuarios_registrados:
        print("This login already exists. Please try another one.")
    else:
        usuarios_registrados[login_user] = USER(name, login_user, password_user)
        print("User successfully registered!")

def ver_cinemas():
    print("\n--- Choose a Cinema ---")
    for i, cinema_nome in enumerate(cinemas.keys(), 1):
        print(f"{i}. {cinema_nome}")
    print("0. Back to main menu")
    
    while True:
        escolha = input("Enter the theater number: ")
        if escolha == '0':
            return
        try:
            cinema_nome = list(cinemas.keys())[int(escolha) - 1]
            ver_filmes(cinemas[cinema_nome])
            break
        except (ValueError, IndexError):
            print("Invalid option.")
            
def ver_filmes(cinema_obj):
    cinema_obj.list_movies()
        
    if not usuario_logado:
        input("Press Enter to return to the menu...")
        return
        
    escolha_filme = input("Enter the name of the movie you want to buy tickets for (or ‘exit’ to go back): ")
    if escolha_filme.lower() == 'exit':
        return
    
    filme_selecionado = next((m for m in cinema_obj.movies if m.name.lower() == escolha_filme.lower()), None)
    if not filme_selecionado:
        print("Movie not found. Please try again.")
        return
        
    comprar_ingresso(filme_selecionado)

def comprar_ingresso(movie):
    print(f"\n--- Buy Ticket for '{movie.name}' ---")
    movie.list_showtimes()
    
    escolha_horario = input("Enter the session time (ex: 19:00): ")
    showtime_selecionado = next((s for s in movie.showtimes if s.time == escolha_horario), None)
    
    if not showtime_selecionado:
        print("Invalid time. Please try again.")
        return
        
    print(f"\nSelected time: {showtime_selecionado.time} | Room: {showtime_selecionado.screen_number}")
    showtime_selecionado.list_available_seats()
    
    escolha_assento = input("Enter the number of the seat you want (ex: A5): ")
    assento_selecionado = next((s for s in showtime_selecionado.seats if s.row_and_number.lower() == escolha_assento.lower()), None)
    
    if not assento_selecionado or assento_selecionado.is_reserved:
        print("Seat invalid or already reserved.")
        return
    
    tipo_ingresso = input("Enter the ticket type (Standard, Student, Subscriber): ")
    preco = 25.0
    
    ticket = TICKET(f"Ticket {tipo_ingresso}", preco, assento_selecionado, showtime_selecionado)
    ticket.promotion() #polimorfismo

    print(f"\nPurchase Summary:")
    print(f"Movie: {movie.name}")
    print(f"Session: {showtime_selecionado.time} - Room {showtime_selecionado.screen_number}")
    print(f"Seat: {assento_selecionado.row_and_number}")
    print(f"Price: R$ {ticket.price:.2f}")

    escolha_combo = input("Would you like to add a popcorn combo? (Y/N): ")
    if escolha_combo.lower() == "y":
        combo_size = input("Popcorn size (S, M, L): ").upper()
        popcorn = POPCORN("Popcorn", 0.0, combo_size)
        popcorn.purchase_product()
        print(f"Combo of {popcorn.name} ({popcorn.size}) added. Price: R$ {popcorn.price:.2f}")
        ticket.price += popcorn.price

    pagar = input(f"Total price: R$ {ticket.price:.2f}. Do you wish to proceed with the payment? (Y/N): ")
    if pagar.lower() == "y":
        ticket.purchase_product()
        usuario_logado.add_booking(ticket)
        print("\nPayment processed and reservation confirmed!")
    else:
        print("Purchase canceled.")

def avaliar_filme():
    if not usuario_logado:
        print("You must be logged in to rate a movie.")
        return
    
    print("\n--- Choose a Cinema to Rate a Movie ---")
    for i, cinema_nome in enumerate(cinemas.keys(), 1):
        print(f"{i}. {cinema_nome}")
    print("0. Back to main menu")

    while True:
        escolha = input("Enter the theater number: ")
        if escolha == '0':
            return
        try:
            cinema_nome = list(cinemas.keys())[int(escolha) - 1]
            cinema_obj = cinemas[cinema_nome]
            
            print(f"\n--- Movies available on {cinema_obj.name} ---")
            for i, movie in enumerate(cinema_obj.movies, 1):
                print(f"{i}. {movie.name}")
            
            escolha_filme = input("Enter the number of the movie you want to rate: ")
            movie_to_review = cinema_obj.movies[int(escolha_filme) - 1]

            rating = int(input("Your rating (1 a 5): "))
            if rating < 1 or rating > 5:
                raise ValueError
            comment = input("Your comment: ")
            
            movie_to_review.add_review(rating, comment)
            print("Review successfully submitted!")
            return

        except (ValueError, IndexError):
            print("Invalid option. Please try again.")

# --- Iniciar o programa ---
if __name__ == "__main__":
    inicializar_dados()
    menu_principal()