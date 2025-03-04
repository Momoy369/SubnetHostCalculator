import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def calculate_hosts(h):
    return 2 ** h

def calculate_subnets(n):
    return 2 ** n

def main():
    print(Fore.YELLOW + "\nIP Subnet Calculator")
    print(Fore.CYAN + "Masukkan jumlah bit host (h) dan subnet (n)")
    print("Tekan CTRL+C untuk keluar.")
    
    while True:
        try:
            h = int(input(Fore.GREEN + "\nMasukkan jumlah bit host (h): "))
            n = int(input(Fore.GREEN + "Masukkan jumlah bit subnet (n): "))
            
            if h < 0 or n < 0:
                print(Fore.RED + "Error: Jumlah bit tidak boleh negatif. Coba lagi.")
                continue
            
            hosts = calculate_hosts(h)
            subnets = calculate_subnets(n)
            
            print(Fore.MAGENTA + f"Jumlah host yang tersedia: {hosts}")
            print(Fore.MAGENTA + f"Jumlah subnet yang tersedia: {subnets}")
        
        except ValueError:
            print(Fore.RED + "Error: Harap masukkan angka yang valid.")
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nKeluar dari program. Sampai jumpa!")
            break

if __name__ == "__main__":
    main()
