# Laboratóriumi Mérési Útmutató: HTTP Protokoll és Csomaghallgatás Vizsgálata

**Tárgy:** Hálózati Fejlesztés és Biztonság  
**Mérés címe:** HTTP GET és POST metódusok összehasonlítása Cisco SPAN port és Wireshark segítségével  
**Időtartam:** 2 óra (90 perc)  
**Mérési szint:** Egyetemi / Szakképzési gyakorlat  

---

## 1. A mérés célja

A mérés során a hallgatók gyakorlati betekintést nyernek a nem titkosított (HTTP) hálózati forgalom sérülékenységeibe. A feladat bemutatja:
1. A **HTTP GET** és **HTTP POST** kérések szerkezeti különbségeit.
2. A **Cisco SPAN (Switched Port Analyzer)** porttükrözési technológia beállítását és működését.
3. A hálózati adatok elfogását és elemzését **Wireshark** és **Kali Linux** környezetben.
4. A nyílt szövegű (plaintext) jelszóátvitel kockázatait és a HTTPS (TLS/SSL) szükségességét.

---

## 2. Szükséges eszközök és hálózati topológia

### Eszközigény
* **1 db Cisco L2/L3 Switch** (pl. Cisco Catalyst 2960 vagy 3560)
* **1 db Webszerver** (Apache/Nginx + PHP környezet, beállított `index.php` bejelentkezési lappal)
* **1 db Kliens gép** (Bármilyen operációs rendszer böngészővel)
* **1 db Elemző gép** (Kali Linux / Wireshark szoftverrel)
* **UTP patch kábelek**

### Hálózati Topológia

```text
       +-----------------------+
       |   Cisco Switch 2960   |
       +-----------------------+
         |         |         |
     Fa0/1       Fa0/2     Fa0/24
       |           |         | (SPAN Destination)
       v           v         v
+------------+ +-------+ +------------+
| Kliens gép | | Szerver| | Kali Linux |
| 192.168.1.10||192.168.1.50|| (Wireshark)|
+------------+ +-------+ +------------+
```

---

## 3. Elméleti áttekintés

### HTTP GET vs. POST
* **GET metódus:** Az elküldött adatok a kérés URL-jében (query string) jelennek meg. Az adatok láthatóak a böngésző címsorában, a proxy naplókban és a böngészési előzményekben.
* **POST metódus:** Az adatok a HTTP kérés törzsében (HTTP Request Body) utaznak. Nem láthatók az URL-ben, de titkosítás hiányában a hálózaton továbbra is nyílt szövegként továbbítódnak.

### Cisco SPAN (Port Mirroring)
A switcheken alapesetben a portok izolálva vannak: az A portra érkező forgalom csak a B portra megy tovább (amennyiben a cél MAC cím ott található). A SPAN (Switched Port Analyzer) lehetővé teszi, hogy egy vagy több forrásport (Source) forgalmáról másolatot küldjünk egy kijelölt elemző portra (Destination).

---

## 4. Mérési feladatok

### 1. Feladat: A tesztkörnyezet ellenőrzése
1. Csatlakoztassa a kliens gépet a switch **FastEthernet 0/1** portjára.
2. Csatlakoztassa a webszervert a switch **FastEthernet 0/2** portjára.
3. Ellenőrizze a hálózati kapcsolatot: a kliensről érje el a webszerver bejelentkezési oldalát a böngészőben:
   `http://192.168.1.50/index.php`

---

### 2. Feladat: Cisco SPAN (Port Tükrözés) Konfigurációja
Lépjen be a Cisco switch parancssorába (CLI), és állítsa be a tükrözési munkamenetet:

```text
Switch> enable
Switch# configure terminal
Switch(config)# monitor session 1 source interface FastEthernet 0/1 both
Switch(config)# monitor session 1 destination interface FastEthernet 0/24
Switch(config)# end
Switch# show monitor session 1
```

> **Magyarázat:**  
> * A `source interface FastEthernet 0/1 both` utasítás a kliens portjának mindkét irányú (be- és kimenő) forgalmát másolja.  
> * A `destination interface FastEthernet 0/24` utasítás a másolt csomagokat a Kali Linux felé továbbítja.

---

### 3. Feladat: Csomaghalászat Kali Linux / Wireshark segítségével
1. Csatlakoztassa a Kali Linux gépet a switch **FastEthernet 0/24** portjára.
2. Indítsa el a **Wireshark** alkalmazást root joggal:
   ```bash
   sudo wireshark
   ```
3. Válassza ki a megfelelő hálózati interfészt (pl. `eth0`), és indítsa el a csomagbefogást.
4. Állítsa be a kijelzési szűrőt:
   ```text
   http
   ```

---

### 4. Feladat: HTTP GET kérés elemzése
1. A kliens gépen használja a **HTTP GET** bejelentkezési űrlapot.
   * Felhasználónév: `teszt_get`
   * Jelszó: `TitkosJelszo123`
2. Keresse meg a Wireshark-ban az ehhez tartozó `GET /index.php?username_get=...` csomagot.
3. **Mérési tapasztalat rögzítése:**
   * Vizsgálja meg az **Hypertext Transfer Protocol** szakaszt a Wireshark-ban.
   * Jegyezze fel, hol és milyen formában jelenik meg a jelszó!

---

### 5. Feladat: HTTP POST kérés elemzése
1. A kliens gépen használja a **HTTP POST** bejelentkezési űrlapot.
   * Felhasználónév: `teszt_post`
   * Jelszó: `SzigoruanTitkos456`
2. Keresse meg a Wireshark-ban a `POST /index.php` kérést.
3. Nyissa ki a **HTML Form URL Encoded** elemet a csomagrészletekben.
4. **Mérési tapasztalat rögzítése:**
   * Rejtve maradt-e a jelszó a hálózaton elkapott csomagban?
   * Mi a különbség a GET és a POST kérés szerkezete között?

---

## 5. Ellenőrző kérdések a jegyzőkönyvhöz

1. **Biztonságos-e a HTTP POST használata önmagában jelszavak küldésére? Indokolja válaszát!**
2. **Mi a különbség aközött, ahogyan a böngésző címsora kezeli a GET és a POST adatokat?**
3. **Hogyan védhető meg a bejelentkezési folyamat az ilyen jellegű lehallgatástól (Eavesdropping)?**
4. **Mi a szerepe a Cisco SPAN funkciónak az ellenőrzött hálózati monitorozásban és IDS/IPS rendszereknél?**

---

## 6. Segítség

```Wireshark
ip.addr == 192.168.1.50 && http — Csak a megadott webszerverhez tartozó HTTP forgalom.
tcp.port == 80 — A 80-as (HTTP) porton áthaladó teljes TCP forgalom.
http.request.method == "GET" || http.request.method == "POST" — A GET és POST kéréseket egyaránt megjeleníti.
http.request.uri contains "password_get" — Olyan GET kérés, amelynek az URL-jében szerepel a password_get paraméter.
urlencoded-form — A POST kérések során elküldött application/x-www-form-urlencoded törzzsel rendelkező csomagokat mutatja.
````
Érdekes megnézni még
```wireshark
http.user_agent — Megmutatja a kliens böngészőjének típusát, verzióját és az operációs rendszert (pl. Windows, Linux, Android).
http.response.code == 200 — Csak a sikeres szerverválaszokat mutatja.
http.response.code >= 400 — Hibás kéréseket (pl. 404 Not Found, 500 Internal Server Error) szűr ki.
http.server — A webszerver által küldött válaszfejléc, amely felfedi a webszerver szoftvert és annak verzióját (pl. Apache/2.4.52 (Ubuntu)).
arp — Kiszűri a hálózati címfeloldási (Address Resolution Protocol) kéréseket és válaszokat.
eth.addr == xx:xx:xx:xx:xx:xx — Egy konkrét hálózati kártya (MAC-cím) teljes forgalma.
http.content_length > 0 — Kizárólag azokat a HTTP csomagokat mutatja, amelyek érdemi adat-törzzsel (body) rendelkeznek.
frame.len > 500 — A nagyobb méretű hálózati kereteket szűri ki.

````
