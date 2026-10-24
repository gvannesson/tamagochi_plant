
from utils import demander_nombre_entier_positif
from plante import MaPlante

from aptos import main

from utils import charger_excel

chemin_fichier = ("MTG.xlsx") 
df = charger_excel(chemin_fichier)
df_filtre = df[df['label'] == 'FababeanLeaf']  

##############################################################""


import colorama
from colorama import Fore, Style, Back

# Active le support des couleurs dans le terminal (Windows/Mac/Linux)
colorama.just_fix_windows_console()

def tamogochi_plant():
    plante = f"""{Fore.LIGHTGREEN_EX}⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⡶⠖⣶⠤⢀⠀⠀⠀
⠀⠀⠀⠀⢀⣠⡴⠚⡉⠡⢈⠙⢦⣴⠞⠛⠳⣦⡘⠛⢩⣿⣦⠀
⠀⠀⠀⠀⠛⠷⢤⣴⣀⣁⣂⣬⣼⣇⣤⡌⠐⢈⠻⡦⠘⠛⡛⣧
⠀⠀⠀⠀⡀⠀⣶⠶⠻⢧⡀⢹⣻⡟⣿⠃⣾⣧⠁⣰⣄⠙⣿⣛
⠀⢀⣴⣾⡝⠛⠛⣀⣴⣾⠧⢼⣯⣧⣿⡷⠇⣻⣀⣯⢹⡀⢄⡿
⢀⡤⠶⠖⠋⣐⣴⠟⠁⡀⠄⡂⠈⣿⣿⠶⠶⢦⣍⠉⠈⠙⠛⠁{Fore.GREEN}
⡾⠷⢶⡌⠐⠈⡁⢄⣂⡰⢸⡿⣦⣿⣿⢀⠐⡀⠌⣧⠀⠀⠀⠀
⢴⠛⠉⢰⡟⣧⠀⣸⡟⣇⢈⣷⢹⣿⣿⢦⣔⡀⢂⣿⠀⠀⠀⠀
⠸⢦⣥⡾⠁⠿⣤⠼⠇⠛⠋⠀⠀⣿⣿⠀⠈⠉⠉⠁⠀⠀⠀⠀{Fore.RED}
⠀⠀⠀⠀⠀⠀⠀⢸⡏⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⣻⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠓⣶⠶⠶⠶⠶⠶⠶⠶⠶⣶⠛⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠀⠀⠀⠀⠀⠀⢠⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⠒⠒⠖⠲⠒⠒⠛⠀⠀⠀⠀⠀⠀{Style.RESET_ALL}"""

    print("\n" + f"{Fore.CYAN}{Style.BRIGHT}═══ 🌱 TAMAGOCHI PLANT 🌱 ═══{Style.RESET_ALL}")
    print(plante)
    print(f"{Style.RESET_ALL}{Fore.CYAN}═══════════════════════════════════════════{Style.RESET_ALL}\n")

if __name__ == "__main__":
    tamogochi_plant()

#########################################################################################################################

print("""𝙱𝚒𝚎𝚗𝚟𝚎𝚗𝚞𝚎 𝚍𝚊𝚗𝚜 𝚝𝚘𝚗 𝚃𝚊𝚖𝚊𝚐𝚘𝚌𝚑𝚒 𝙿𝚕𝚊𝚗𝚝 🪴
𝑇𝑜𝑛 𝑏𝑢𝑡 : 𝑃𝑟𝑒n𝑑𝑟𝑒 𝑠𝑜𝑖𝑛 𝑑𝑒 𝑡𝑜𝑛 𝑎𝑚𝑖𝑒 𝑙𝑎 𝑝𝑙𝑎𝑛𝑡𝑒 🥰""")

nom_plante = input('💗 𝙳𝚘𝚗𝚗𝚎 𝚞𝚗 𝚗𝚘𝚖 𝚊 𝚝𝚊 𝚙𝚕𝚊𝚗𝚝𝚎 : ') 
feuilles = len(df_filtre)

print(f"{Style.RESET_ALL}{Fore.CYAN}═══════════════════════════════════════════{Style.RESET_ALL}\n")

plant = MaPlante(nom_plante, feuilles)
print(plant)

nb_tours = 0
while plant.est_vivante():
        plant.calcul_azote()
        ajout_eau = demander_nombre_entier_positif("💦 𝙰𝚟𝚎𝚌 𝚌𝚘𝚖𝚋𝚒𝚎𝚗 𝚍𝚎 𝚖𝚕 𝚍'𝚎𝚊𝚞 𝚊𝚛𝚛𝚘𝚜𝚎𝚜 𝚝𝚞 𝚝𝚊 𝚙𝚕𝚊𝚗𝚝𝚎 ? ", 0)
        ajout_engrais = demander_nombre_entier_positif("💩 𝙲𝚘𝚖𝚋𝚒𝚎𝚗 𝚍𝚎 𝚐 𝚍'𝚎𝚗𝚐𝚛𝚊𝚒𝚜 𝚍𝚘𝚗𝚗𝚎𝚜 𝚝𝚞 𝚊 𝚝𝚊 𝚙𝚕𝚊𝚗𝚝𝚎 ? ", 0)
        plant.recevoir_eau(ajout_eau)
        plant.recevoir_engrais(ajout_engrais)
        plant.consommation_eau()
        plant.consommation_engrais()
        plant.mettre_a_jour_sante()
        nb_tours += 1
        print(plant.donner_indices())
        print(f'Ta plante a {int(plant.niveau_engrais)} en engrais !')
        print(f'Ta plante a {plant.niveau_eau} en eau !')
        print(f'Ta plante a {plant.points_sante} points de santé !')
        

        main.Run.faba_bean_plant_simulation(default = None, initial_step = 0, final_step = (nb_tours))

        print(f"{Style.RESET_ALL}{Fore.CYAN}═══════════════════════════════════════════{Style.RESET_ALL}\n")


print(f'𝔱𝔞 𝔭𝔩𝔞𝔫𝔱𝔢 𝔢𝔰𝔱 𝔪𝔬𝔯𝔱𝔢 𝔞𝔲 𝔟𝔬𝔲𝔱 𝔡𝔢 {𝔫𝔟_𝔱𝔬𝔲𝔯𝔰} 𝔧𝔬𝔲𝔯𝔰  🥺')