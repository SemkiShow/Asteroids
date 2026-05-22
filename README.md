# Asteroids

## Wymagania systemowe

> [!WARNING]
> Terminal powinien wspierać kody ANSI. Uwaga: terminal środowiska IDLE nie posiada wsparcia kodów ANSI!

Zaleca się uruchamiać program w terminalu, który wspiera Unicode oraz kody ANSI w pełni. Przykładami takich terminalów na systemie Windows są (Git) Bash oraz Windows Terminal. W przypadku uzycia terminalu, który nie wspiera Unicode i/lub kodów ANSI w pełni, program może działać niepoprawnie.

Zauważono także, że terminale na Linuxie pozwalają osiągnąć lepszych wyników kratek na sekundę, niż terminale na Windowsie. Jeśli jest możliwość testowania na Linuxie, to zaleca się z niej skorzystać dla jeszcze lepszego doświadczenia.

### Najlepszy setup

- Terminal: szybki z pełnym wsparciem Unicode i ANSI
- Czcionka terminalu: [Nerd font](https://www.nerdfonts.com/)

## Instrukcje uruchomienia

```bash
python main.py
```

## O grze

Jesteś statkiem kosmicznym. Twoim celem jest dotarcie do celu, unikając asteroid i zbierając punkty. Nie zapomnij, że paliwo może się skończyć!

### Sterowanie interfejsem graficznym

Aby wybrać widżet (przycisk, pole tekstowe, itp.), należy użyć klawisz starzałek. Wybrany widżet będzie wyodrębniony kolorem.  
Aby kliknąć przycisk należy nacisnąć klawisz Enter.  
Aby zmienić wybrany element w liście rozwijanej lub zmienić wartość suwaka należy nacisnąć Enter. Wtedy widżet podświeci się niebieskim kolorem. Aby powrócić do wyboru widżetów należy nacisnąć Enter jeszcze raz.

### Menu główne

```text
         _        _                 _     _          
        / \   ___| |_ ___ _ __ ___ (_) __| |___      
       / _ \ / __| __/ _ \ '__/ _ \| |/ _` / __|     
      / ___ \\__ \ ||  __/ | | (_) | | (_| \__ \     
     /_/   \_\___/\__\___|_|  \___/|_|\__,_|___/     
                                                     
                                                     
                        Play                         
                                                     
                      Settings                       
                                                     
                        Exit                         
```

Wciśnięcie przycisku `Play` powoduje uruchomienie [gry](#menu-gry).  
`Settings` otwiera [menu ustawień](#menu-ustawień)
`Exit` zamyka program

### Menu ustawień

```text
Back                                                 
                                                     
Player name    Player                                
                                                     
Difficulty     Easy                                  
                                                     
Map size X     -------+------------ 200              
                                                     
Map size Y     -------+------------ 200              
```

W danym menu można zmienić nazwę gracza, poziom trudności gry (Easy, Medium lub Hard) oraz wymiary mapy (50-500).  
Wciśnięcie przycisku `Back` powoduje powrót do menu głównego.

Ustawienia są zapisywne do pliku `settings.json`.

### Menu gry

```text
Player: Player                                       
Position: 163.4 53.1                                 
Speed: 0                                             
Fuel: 838.2                               ?          
Points: 0                                            
Time: 15.8s                                          
Frame: 490                                           
                                                     
     #  #                 ↑                          
                    X                                
```

Sterowanie graczem (`↑` na obrazku) odbywa się za pomocą strzałek w lewo/prawo lub A/D (zmiana kątu) oraz spacji (przyspieszenie statku).

Podczas gry są 3 typy pól oprócz pola pustego i pola poza granicą świata: asteroida (`#` na obrazku), pole o wyniku niewiadomym (`?` na obrazku) oraz cel (`X` na obrazku).  
Granica świata jest oznaczona czerwonym wypełnieniem.  
Kontakt z polem poza granicą świata lub asteroidą powoduje natychmiastowy [koniec gry](#koniec-gry).  
[Koniec gry](#koniec-gry) może także być spowodowany brakiem paliwa w statku (Pole `Fuel` w lewym górnym rogu ekranu).  
Kontakt z polem o wyniku niewiadomym powoduje losowe wydarzenie: zmianę liczby punktów (+ 10-50 lub - 10-30), zmianę licznika czasu (+- 1-3 sekundy) lub dodanie paliwa do statku (+ 100-500).  

W oknie turtle są pokazane obecna pozycja gracza oraz położenie celu.  

Wciśnięcie klawiszu Escape powoduje zatrzymanie gry oraz otwarcie [menu pauzy](#menu-pauzy)

### Menu pauzy

```text
        Paused       
                     
    Back to game     
       Restart       
      New game       
 Return to main menu 
```

Przycisk `Back to game` pozwala wrócić do menu gry, `Restart` uruchamia grę ponownie, `New game` tworzy nową grę, `Return to main menu` powoduje powrót do menu głównego.

### Koniec gry

```text
      Game Over!     
                     
    Player: Player   
  Map size: 200 200  
  Start pos: 174 77  
    End pos: 0 56    
    Time: 144.0s     
    Frames: 4397     
    End speed: 0     
     Fuel: 714.8     
      Points: 0      
    Fields: 0/15     
  Difficulty: Medium 
                     
       Restart       
      New game       
 Return to main menu 
```

Przycisk `Restart` uruchamia grę ponownie, `New game` tworzy nową grę, `Return to main menu` powoduje powrót do menu głównego.

### Zwycięstwo

```text
      You won!       
                     
    Player: Player   
  Map size: 200 200  
   Start pos: 1 42   
   End pos: 179 42   
      Time: 8.0s     
     Frames: 243     
    End speed: 0     
     Fuel: 794.2     
      Points: 0      
    Fields: 0/29     
  Difficulty: Hard   
                     
      New game       
 Return to main menu 
```

Przycisk `New game` tworzy nową grę, `Return to main menu` powoduje powrót do menu głównego.
