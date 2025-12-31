import random


class Train:
    def __init__(self, train_no, name, stations, seats, rate_per_km):
        self.train_no = train_no
        self.name = name
        self.stations = stations      
        self.seats = seats            
        self.rate_per_km = rate_per_km

    def show_train_info(self):
        print(f"\n Train No: {self.train_no}, Name: {self.name}")
        print("Stations on Route:")
        for station, dist in self.stations.items():
            print(f"  {station} ({dist} KM)")
        print("Available Seats:", self.seats)

    def calculate_fare(self, start, end, coach):
        if start not in self.stations or end not in self.stations:
            return None
        start_dist = self.stations[start]
        end_dist = self.stations[end]

        
        distance = abs(end_dist - start_dist)
        if distance == 0:
            return None

        base_fare = distance * self.rate_per_km
        class_multiplier = {
            "SL": 1.0,
            "3AC": 1.5,
            "2AC": 2.0,
            "1AC": 3.0
        }
        return base_fare * class_multiplier.get(coach, 1)


class BookingSystem:
    def __init__(self):
        self.trains = []
        self.bookings = []

    def add_train(self, train):
        self.trains.append(train)

    def show_trains(self):
        print("\n--- Available Trains ---")
        for train in self.trains:
            train.show_train_info()

    def apply_quota_discount(self, fare, quota):
        discounts = {
            "ARMY": 0.5,
            "DISABLED": 0.4,
            "LADIES": 0.2,
            "SENIOR": 0.3
        }
        return fare * (1 - discounts.get(quota, 0))

    def process_payment(self, final_fare):
        print("\n Payment Options:")
        print("1. Card\n2. UPI\n3. Wallet\nType 'exit' to cancel")
        choice = input("Choose payment method: ")

        if choice.lower() == "exit":
            print(" Payment Cancelled.")
            return False

        if choice in ["1", "2", "3"]:
            mobile = input("Enter mobile number for OTP : ")
            if mobile.lower() == "exit":
                print(" Payment Cancelled.")
                return False

            otp = random.randint(1000, 9999)
            print(f" OTP sent to {mobile}: {otp}")
            entered = input("Enter OTP : ")

            if entered.lower() == "exit":
                print(" Payment Cancelled.")
                return False

            if int(entered) == otp:
                print(" Payment Successful! Enjoy your journey ")
                return True
            else:
                print(" Payment Failed! Incorrect OTP.")
                return False
        else:
            print(" Invalid payment option!")
            return False

    def book_ticket(self, train_no, passenger_name, coach_class, quota, start, end, seat_count):
        for train in self.trains:
            if train.train_no == train_no:
                if train.seats.get(coach_class, 0) >= seat_count:
                    fare = train.calculate_fare(start, end, coach_class)
                    if fare is None:
                        print(" Invalid station selection. Please check start/end stations.")
                        return

                    total_fare = fare * seat_count
                    final_fare = self.apply_quota_discount(total_fare, quota)

                    print(f"\n Base Fare (for {seat_count} seat(s)): ₹{total_fare:.2f}")
                    if quota != "NONE":
                        print(f" Quota '{quota}' applied! Discounted Fare: ₹{final_fare:.2f}")
                    else:
                        print(f"Final Fare: ₹{final_fare:.2f}")

                    confirm = input("Proceed to payment? (yes/no/exit): ").lower()
                    if confirm in ["exit", "no"]:
                        print(" Booking Cancelled.")
                        return

                    if not self.process_payment(final_fare):
                        print(" Booking Failed due to payment issue.")
                        return

                    train.seats[coach_class] -= seat_count
                    booking = {
                        "Passenger": passenger_name,
                        "Train": train.name,
                        "From": start,
                        "To": end,
                        "Class": coach_class,
                        "Quota": quota,
                        "Seats": seat_count,
                        "Fare": final_fare
                    }
                    self.bookings.append(booking)
                    print(f"\n Ticket Booked Successfully for : {passenger_name}")
                    print("Booking Details:", booking)
                    return
                else:
                    print(f"\n Not enough seats! Only {train.seats.get(coach_class, 0)} available in {coach_class}.")
                    return
        print("\n Train not found.")

    def show_bookings(self):
        print("\n=== All Bookings ===")
        if not self.bookings:
            print("No bookings yet.")
        for booking in self.bookings:
            print(booking)



system = BookingSystem()


t1 = Train(101, "Central Local",
           {"Mumbai": 0, "Dadar": 10, "Kurla": 20, "Thane": 35, "Dombivli": 50, "Kalyan": 60},
           {"SL": 10, "3AC": 5, "2AC": 3, "1AC": 2}, rate_per_km=2)

t2 = Train(202, "Harbour Local",
           {"Panvel": 0, "Belapur": 12, "Nerul": 22, "Vashi": 30, "Kurla": 45, "Mumbai": 55},
           {"SL": 15, "3AC": 6, "2AC": 4, "1AC": 2}, rate_per_km=2)

t3 = Train(303, "Uran Local",
           {"Nerul": 0, "Seawoods Darave": 2, "Belapur": 4, "Bamandongri": 8, "Kharkopar": 12,
            "Nhava Sheva": 24, "Dronagiri": 27, "Uran": 30},
           {"SL": 15, "3AC": 6, "2AC": 4, "1AC": 2}, rate_per_km=2)

system.add_train(t1)
system.add_train(t2)
system.add_train(t3)


while True:
    print("\n---- Train Ticket Booking System ---")
    print("1. Show Trains")
    print("2. Book Ticket")
    print("3. Show Bookings")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        system.show_trains()
    elif choice == "2":
        passenger = input("Enter Passenger Name: ")
        if passenger.lower() == "exit":
            continue

        try:
            train_no = int(input("Enter Train No : "))
        except ValueError:
            print(" Invalid input!")
            continue

        coach = input("Enter Class (SL/3AC/2AC/1AC): ").upper()
        if coach == "EXIT":
            continue

        print("\nAvailable Quotas: NONE / ARMY / DISABLED / LADIES / SENIOR")
        quota = input("Enter Quota : ").upper()
        if quota == "EXIT":
            continue

        start = input("Enter Starting Station: ").strip().title()
        if start.lower() == "exit":
            continue
        end = input("Enter Destination Station: ").strip().title()
        if end.lower() == "exit":
            continue

        try:
            seat_count = int(input("Enter number of seats: "))
        except ValueError:
            print(" Invalid seat number!")
            continue

        system.book_ticket(train_no, passenger, coach, quota, start, end, seat_count)

    elif choice == "3":
        system.show_bookings()
    elif choice == "4":
        print(" Thank you for using Train Booking System ")
        break
    else:
        print(" Invalid choice! Try again.")
