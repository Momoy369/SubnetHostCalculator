import ipaddress
import math
import colorama
import csv
import os
from colorama import Fore, Style

colorama.init(autoreset=True)

def calculate_subnet(network, num_subnets=None, num_hosts=None, export=False):
    try:
        net = ipaddress.IPv4Network(network, strict=False)
        prefix = net.prefixlen
        total_host_bits = 32 - prefix
        
        print(f"\n{Fore.CYAN}📌 Network awal: {network} ({net.netmask})")
        print(f"{Fore.YELLOW}🔍 Menganalisis subnetting...\n")
        
        if num_hosts:
            needed_host_bits = math.ceil(math.log2(num_hosts + 2))
            new_prefix = 32 - needed_host_bits
            num_subnets = 2 ** (new_prefix - prefix)
        elif num_subnets:
            needed_subnet_bits = math.ceil(math.log2(num_subnets))
            new_prefix = prefix + needed_subnet_bits
        else:
            print(f"{Fore.RED}❌ ERROR: Harap masukkan jumlah subnet atau jumlah host yang dibutuhkan!\n")
            return

        new_netmask = ipaddress.IPv4Network(f"0.0.0.0/{new_prefix}").netmask
        usable_hosts = (2 ** (32 - new_prefix)) - 2
        num_available_subnets = 2 ** (new_prefix - prefix)

        print(f"{Fore.GREEN}✅ Subnet mask baru: {new_netmask} (/ {new_prefix})")
        print(f"✅ Jumlah subnet yang terbentuk: {num_available_subnets} subnet")
        print(f"✅ Jumlah host per subnet: {usable_hosts} host usable\n")

        print(f"{Fore.MAGENTA}📜 Daftar Subnet yang Terbentuk:")
        print(f"{Fore.MAGENTA}{'-'*72}")
        print(f"{'Subnet':<10}{'Network Address':<18}{'Host Range':<32}{'Broadcast Address'}")
        print(f"{'-'*72}")

        subnet_list = list(net.subnets(new_prefix=new_prefix))[:num_subnets]
        results = []
        
        for i, subnet in enumerate(subnet_list, start=1):
            network_address = str(subnet.network_address)
            broadcast_address = str(subnet.broadcast_address)
            first_host = str(subnet.network_address + 1)
            last_host = str(subnet.broadcast_address - 1)
            
            print(f"{Fore.CYAN}{i:<10}{network_address:<18}{first_host} - {last_host:<22}{broadcast_address}")
            results.append([i, network_address, first_host, last_host, broadcast_address])
        
        print(f"{Fore.MAGENTA}{'-'*72}\n")
        
        if export:
            export_results(results, network)

    except ValueError as e:
        print(f"{Fore.RED}❌ ERROR: {e}")

def export_results(results, network):
    folder_name = "subnet_results"
    os.makedirs(folder_name, exist_ok=True)
    
    filename_txt = os.path.join(folder_name, f"subnet_{network.replace('/', '_')}.txt")
    filename_csv = os.path.join(folder_name, f"subnet_{network.replace('/', '_')}.csv")
    
    with open(filename_txt, 'w') as txt_file, open(filename_csv, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Subnet", "Network Address", "First Host", "Last Host", "Broadcast Address"])
        
        txt_file.write("Subnet Calculation Results\n")
        txt_file.write("-"*72 + "\n")
        txt_file.write(f"{'Subnet':<10}{'Network Address':<18}{'Host Range':<32}{'Broadcast Address'}\n")
        txt_file.write("-"*72 + "\n")
        
        for row in results:
            csv_writer.writerow(row)
            txt_file.write(f"{row[0]:<10}{row[1]:<18}{row[2]} - {row[3]:<22}{row[4]}\n")
        
        txt_file.write("-"*72 + "\n")
    
    print(f"{Fore.GREEN}✅ Hasil disimpan di folder '{folder_name}' sebagai: {filename_txt} & {filename_csv}\n")

if __name__ == "__main__":
    print(f"{Fore.BLUE}🔹 SUBNET CALCULATOR 🔹\n")
    
    while True:
        try:
            network_input = input(f"{Fore.CYAN}Masukkan Network (contoh: 192.168.1.0/24): {Fore.RESET}")
            choice = input(f"{Fore.YELLOW}Hitung berdasarkan (1) Subnet atau (2) Host? {Fore.RESET}").strip()
            
            if choice == '1':
                num_subnets = int(input(f"{Fore.YELLOW}Masukkan jumlah subnet yang diinginkan: {Fore.RESET}"))
                num_hosts = None
            elif choice == '2':
                num_hosts = int(input(f"{Fore.YELLOW}Masukkan jumlah host yang dibutuhkan per subnet: {Fore.RESET}"))
                num_subnets = None
            else:
                print(f"{Fore.RED}❌ ERROR: Pilihan tidak valid!\n")
                continue
            
            export = input(f"{Fore.BLUE}Ingin menyimpan hasil ke file? (y/n): {Fore.RESET}").strip().lower() == 'y'
            calculate_subnet(network_input, num_subnets, num_hosts, export)
            
        except ValueError:
            print(f"{Fore.RED}❌ ERROR: Input tidak valid!\n")
        
        again = input(f"{Fore.BLUE}Ingin menghitung lagi? (y/n): {Fore.RESET}").strip().lower()
        if again != 'y':
            print(f"{Fore.GREEN}🚀 Terima kasih! Sampai jumpa!\n")
            break