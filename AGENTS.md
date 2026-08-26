# AGENTS.md, Arbeitsordner Kommune

Diese Datei ist für KI-Agents, die am Wohnprojekt-Dokument arbeiten. Sie ist
Erfahrungswissen aus mehreren langen Sessions, keine Wunschliste. Jede Regel hier
steht drin, weil ihr Fehlen schon einmal Schaden angerichtet hat.

**Lies sie vollständig, bevor du die erste Zeile änderst.**

---

## 1 Was hier liegt

| Datei                                       | Rolle                                                                                    |
| ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `2026-08-25-queeres-wohnprojekt-design.md`  | **Das Dokument.** Einziges Arbeitsziel. UTF-8 **ohne BOM**, Zeilenenden **LF**            |
| `repariere-office-viewer.py`                | Reparaturskript für Formatierungsschäden, siehe Abschnitt 3. Nach **jedem** Edit laufen    |
| `2026-08-26-gestrichene-saetze.md`          | Arbeitsdokument mit Sätzen, die beim Kürzen herausgefallen sind. Nicht anfassen           |
| `*.bak`, `*.vorher.md`                      | Sicherungen. **Niemals ohne Rückfrage löschen**, auch nicht die alten                     |

Das Dokument ist ein Entwurf für ein queeres Wohnprojekt: Finanzierung, Rechtsform,
Governance, Kinderschutz, Quellenverzeichnis. Rund 30.000 Wörter, etwa 136
Überschriften, knapp 500 Tabellenzeilen, 5 Mermaid-Diagramme.

**Arbeitssprache ist Deutsch.** Antworte auf Deutsch, auch wenn die Anfrage englisch ist.

---

## 2 Die harten Regeln

Diese Punkte sind nicht verhandelbar und werden bei jeder Prüfung maschinell kontrolliert.

1. **Null Geviertstriche.** Der Zähler `EmDash` muss `0` bleiben. Zahlenbereiche werden
   ausgeschrieben: „700 bis 850", nicht mit Strich. Halbgeviertstriche als Gedankenstrich
   ebenfalls vermeiden, das Dokument nutzt Kommas und Punkte.
2. **Anführungszeichen sind `„…"`**, also U+201E öffnend und ein **gerades** `"` (U+0022)
   schließend. Typografische Schlusszeichen (U+201C) sind verboten, der Zähler `U+201C`
   muss `0` sein. Zur Falle in Python siehe Abschnitt 5.
3. **Jede Entscheidung, jede Zahl, jede Rechtsnorm, jeder `(→ x.y)`-Verweis und jede Quelle
   bleibt erhalten**, solange sie nicht nachweislich falsch ist. Kürzen heißt: Begründungs-
   prosa straffen, niemals Inhalt entfernen.
4. **Neue Inhalte nur dort, wo der Nutzer sie verlangt hat.** Alles andere ist reine
   Korrekturarbeit. Ein Agent hat einmal einen fachlich passenden Abschnitt angeboten und
   klar ein „nein" bekommen. Ungefragte Ergänzungen sind unerwünscht.
5. **`## Worum es geht` (etwa Zeile 5) ist vom Nutzer selbst geschrieben.** Nicht anfassen.
6. **Abschnitt 8.0 bleibt ausdrücklich unentschieden** (Varianten A/B/C). Nicht auflösen.
7. **bonn.de nicht crawlen.** Die Seite schließt KI-Agenten per robots.txt aus, das wird
   respektiert und ist im Dokument so vermerkt.
8. **Änderungshistorie am Dateiende pflegen.** Jede inhaltliche Runde bekommt eine Zeile
   mit Datum und einer fetten Kurzüberschrift.

### Statusmarker im Quellenverzeichnis

Die Marker in Abschnitt 14.4 sind eine Ehrlichkeitszusage und dürfen nie geraten werden.
Die Legende steht direkt über der Tabelle.

| Marker           | Bedeutung                                                                       |
| ---------------- | ------------------------------------------------------------------------------- |
| `[geprüft]`      | Seite wurde aufgerufen, Inhalt gelesen, Aussage stimmt                          |
| `[Adresse ok]`   | Server antwortet, Inhalt nicht im Detail geprüft                                |
| `[Seite defekt]` | Server antwortet, Seite technisch unbrauchbar. Inhalt ungeprüft, Kontakt anders |
| `[ungeprüft]`    | Keine Bestätigung möglich                                                       |

---

## 3 Der wichtigste Fallstrick: die Datei schreibt sich selbst um

Die VS-Code-Erweiterung **`cweijan.vscode-office` (Office Viewer)** registriert sich als
**Standardeditor für `*.md`** und ist ein WYSIWYG-Editor. Schon das bloße Öffnen und
Speichern serialisiert die Datei neu. Sie frisst dabei das Leerzeichen vor Hervorhebungen
(`mit **Direktlinks**` wird zu `mit**Direktlinks**`) und polstert Tabellenzellen um.

- Das ist **mehrfach passiert**, einmal mit 52 Schäden auf einen Schlag.
- Gegenmittel steht in den Nutzereinstellungen:
  `"workbench.editorAssociations": {"*.md": "default", "*.markdown": "default"}`
- **Diese Einstellung greift erst nach „Reload Window" oder erneutem Öffnen des Tabs.**
  Wenn der Nutzer das Dokument offen hat, kann sie wirkungslos sein.
- Erkennungsregex (die naive Variante, die nur auf `**` prüft, meldete fälschlich
  „alles sauber", während 50 Schäden existierten):

  ```
  (?<=[\p{L}\p{N},;:\.\)])(\*{1,2})(?=[\p{L}\p{N}])
  ```

- **Blindes Ersetzen durch `' $1'` ist falsch**, weil das schließende Zeichen ein
  Leerzeichen an der falschen Seite bekäme (`**fett**Wort` würde zu `**fett** **Wort`).
  Das mitgelieferte `repariere-office-viewer.py` zählt deshalb die Parität je Zeile und
  setzt das Leerzeichen davor nur bei öffnenden, dahinter nur bei schließenden Läufen.

### Der Sternchen-Detektor hat eine Lücke: Links

Der Editor frisst das Leerzeichen auch **vor Markdown-Links**, und der Regex oben sieht das
nicht, weil er nur Sternchen kennt. Am 26.08.2026 lagen deshalb vier unentdeckte Schäden im
Dokument, unter anderem `in Köln etwa[**Zartbitter e. V.**](...)` in 8.2 und drei Einträge
in 14.5. Zweiter Detektor, zusätzlich laufen lassen:

```
(?<=[\p{L}\p{N},;:\.\)])\[[^\]\[]+\]\(
```

Das abschließende `](` ist entscheidend. Ohne diesen Teil trifft das Muster auch die
**Mermaid-Knoten** der Form `K["<b>Trägerkreis</b>"]`, die völlig in Ordnung sind. Ungefiltert
waren es 29 Treffer, davon 25 harmlos. Reparatur ist hier simpel, weil ein Link nur eine
öffnende Klammer hat: Leerzeichen davor einfügen, Parität spielt keine Rolle.

**Gegenprobe nach jeder Leerzeichen-Reparatur:** Der Text ohne alle Leerzeichen muss vorher
und nachher identisch sein (`alt.replace(" ","") == neu.replace(" ","")`). Ist er es nicht,
hat die Regex Inhalt angefasst.

**Konsequenz für dich:** Nach jedem Edit das Reparaturskript laufen lassen und **beide**
Zähler prüfen. `Artefakte` und `LinkArtefakte` müssen `0` sein, dazu `Reparaturen: 0`.

> **Beide Detektoren nicht auf diese Datei anwenden.** Die Schadensbeispiele hier sind
> absichtlich kaputt, damit man sie sieht, und die zitierten Regex-Muster erzeugen weitere
> Treffer: `(?<![0-9])4\.[345](?![0-9])` aus Abschnitt 5 sieht für den Link-Detektor aus wie
> `[345](`. Die Detektoren melden in dieser AGENTS.md also zwangsläufig einige Treffer, und
> das ist richtig so. Eine konkrete Sollzahl steht hier bewusst nicht, weil jede Bearbeitung
> dieses Absatzes sie sofort verschieben würde. Das Reparaturskript gehört ausschließlich auf
> das Design-Dokument, dort ist der Sollwert für beide Zähler `0`.

Nebenbefund, damit ihn niemand erneut untersuchen muss: **Ruff ab Version 0.16 kann
Markdown**, formatiert aber ausschließlich ` ```python `-Blöcke um. Tabellen und
Hervorhebungen bleiben byte-identisch. Ruff ist **nicht** die Ursache der Schäden.

---

## 4 Der Prüfbefehl nach jedem Edit

Eine Zeile, immer dieselbe. Sie formatiert, repariert und misst in einem Durchgang.

````powershell
$f = "c:\Users\CVBYW\Documents\Kommune\2026-08-25-queeres-wohnprojekt-design.md"; npx --quiet prettier@2.8.8 --write --prose-wrap preserve $f 2>&1 | Select-Object -Last 1; python "c:\Users\CVBYW\Documents\Kommune\repariere-office-viewer.py"; $t = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8); "Woerter=" + [regex]::Matches($t,'\S+').Count + " | Ueberschriften=" + [regex]::Matches($t,'(?m)^#{1,4} ').Count + " | Tabellenzeilen=" + [regex]::Matches($t,'(?m)^\|').Count + " | Mermaid=" + [regex]::Matches($t,'```mermaid').Count + " | Artefakte=" + [regex]::Matches($t,'(?<=[\p{L}\p{N},;:\.\)])(\*{1,2})(?=[\p{L}\p{N}])').Count + " | LinkArtefakte=" + [regex]::Matches($t,'(?<=[\p{L}\p{N},;:\.\)])\[[^\]\[]+\]\(').Count + " | EmDash=" + ($t.Split([char]0x2014).Count - 1) + " | Unbalanciert=" + ([regex]::Matches($t,'(?m)^.*$') | Where-Object { ($_.Value.Split('*').Count - 1) % 2 -eq 1 }).Count + " | U+201C=" + ($t.Split([char]0x201C).Count - 1)
````

**Sollwerte:** `Artefakte=0`, `LinkArtefakte=0`, `EmDash=0`, `Unbalanciert=0`, `U+201C=0`,
`Reparaturen: 0`.
Wörter, Überschriften, Tabellenzeilen und Mermaid dienen als Plausibilitätsanker: Sie
dürfen sich nur so ändern, wie deine Bearbeitung es erklärt. Eine unerwartet gefallene
Tabellenzeilenzahl heißt, dass eine Regex zu viel gefressen hat.

Die Umgebung hat **Node v12.13.0 und npm 6.12.0**, deshalb ist `prettier@2.8.8` gepinnt.
Neuere Versionen laufen dort nicht. Prettier ist auf dieser Datei idempotent.

---

## 5 Wie du das Dokument änderst

**Nie mit Suchen-und-Ersetzen über die ganze Datei, nie freihändig.** Schreib ein kleines
Python-Skript nach `%TEMP%\wohnprojekt\`, das jede Ersetzung einzeln zählt und meldet.
Vorher immer eine Sicherung anlegen: `Copy-Item $f "$f.vor-<name>.bak"`.

```python
# -*- coding: utf-8 -*-
import io, re
F = r"c:\Users\CVBYW\Documents\Kommune\2026-08-25-queeres-wohnprojekt-design.md"
with io.open(F, encoding="utf-8", newline="") as fh: text = fh.read()
ok, fehler = [], []

def ersetze(alt, neu, name, erwartet=1):
    global text
    n = text.count(alt)
    if n != erwartet:
        fehler.append("%s (%d statt %d Treffer)" % (name, n, erwartet)); return
    text = text.replace(alt, neu); ok.append(name)

def zeile(muster, neu, name):          # sichere Variante fuer Tabellenzeilen
    global text
    treffer = re.findall(muster, text, flags=re.M)
    if len(treffer) != 1:
        fehler.append("%s (%d Treffer)" % (name, len(treffer))); return
    text = re.sub(muster, lambda m: neu, text, count=1, flags=re.M); ok.append(name)

def anhaengen(muster, neuezeile, name):
    global text
    treffer = re.findall(muster, text, flags=re.M)
    if len(treffer) != 1:
        fehler.append("%s (%d Treffer)" % (name, len(treffer))); return
    text = re.sub(muster, lambda m: m.group(0) + "\n" + neuezeile, text, count=1, flags=re.M)
    ok.append(name)

# ... hier die Aenderungen ...

with io.open(F, "w", encoding="utf-8", newline="") as fh: fh.write(text)
print("OK     :", "; ".join(ok))
print("FEHLER :", "; ".join(fehler) if fehler else "keine")
```

`newline=""` ist Pflicht, sonst zerschießt Python die LF-Zeilenenden.
Das `lambda m: neu` in `re.sub` ist Absicht: Es verhindert, dass `\1` oder `\g` im
Ersetzungstext als Rückverweis interpretiert werden.

### Fallen, die schon zugeschnappt sind

- **Die Anführungszeichen-Falle, zweimal passiert.** Das schließende Zeichen ist ein
  gerades `"`. In einem Python-String mit doppelten Anführungszeichen beendet es den
  String und erzeugt `SyntaxError: unterminated string literal`. **Schreib immer `\u201e`
  und `\"`, nie die Zeichen literal.**
- **Ein `SyntaxError` im ersten Skript einer Befehlskette stoppt die Kette nicht.** Der
  anschließende Prüfbefehl meldet dann fröhlich grüne Zahlen, obwohl nichts geschrieben
  wurde. **Immer die `OK`/`FEHLER`-Zeile suchen**, nicht nur die Kennzahlen.
- **Prettier polstert Tabellenzellen.** Versuch nie, eine gepolsterte Zeile wörtlich zu
  treffen. Nimm ein Muster wie `^\| \*\*Label\*\*.*$` mit Trefferzähler.
- **Niemals `(?ms)` mit `.*` über einen Tabellenblock.** Das frisst die halbe Datei.
- **Beim Umnummerieren von Abschnitten ist `4.3` in `14.3` ein Falschtreffer.** Immer mit
  Grenzen arbeiten: `(?<![0-9])4\.[345](?![0-9])`.
- **Umlaute sind in `.py` unproblematisch, in `.ps1` nicht.** PowerShell 5.1 liest UTF-8
  ohne BOM als ANSI. In PowerShell-Skripten Sonderzeichen als `[char]0x20AC` (€) oder
  `[char]0xB2` (²) schreiben.
- **Mehrzeiliges PowerShell direkt an das Terminal zu übergeben, zerlegt es.** Schreib eine
  `.ps1` nach `%TEMP%` und ruf sie mit `powershell -ExecutionPolicy Bypass -File` auf.
- **Zeilenenden prüfen, bevor du über Zeilengrenzen hinweg suchst.** Ein Suchmuster mit `\n`
  findet nichts in einer Datei mit CRLF. Der Trefferzähler meldet dann sauber `0 statt 1`,
  was gut ist, aber die Ursache ist nicht offensichtlich. Diese AGENTS.md wurde genau so
  beim ersten Versuch nicht getroffen. Beide Dateien hier sind **LF**.

---

## 6 Recherche im Netz

Die Maschine hängt hinter einem **Zscaler-Proxy**. Das eingebaute Webseiten-Werkzeug
funktioniert dort nicht zuverlässig. Nutze diesen Weg:

```powershell
$wc = New-Object System.Net.WebClient
$wc.Encoding = [System.Text.Encoding]::UTF8
$wc.Proxy = [System.Net.WebRequest]::GetSystemWebProxy()
$wc.Proxy.Credentials = [System.Net.CredentialCache]::DefaultNetworkCredentials
$wc.Headers.Add("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36")
$html = $wc.DownloadString($url)
```

HTML zu Text: `<script|style|nav|footer|head>`-Blöcke entfernen, Tags strippen,
`HtmlDecode`, Leerraum zusammenfassen.

Für Zertifikatsfragen lohnt der direkte TLS-Handschlag über `TcpClient` plus `SslStream`
mit einem Rückruf, der alles akzeptiert. So ließ sich beweisen, dass hinter
`queeres-netzwerk-nrw.de` ein Zertifikat für eine **fremde Domain** liegt, das zudem
**seit 2020 abgelaufen** ist. Die vorherige Vermutung „vermutlich nur ein Artefakt des
Firmennetzes" war damit widerlegt.

### Belegpflicht

- **Suchmaschinen erfinden Daten.** Ein Treffer wurde mit Datum `2026-07-06` geliefert, auf
  der Seite selbst stand `24.04.2024`. **Öffne immer die Seite.**
- DuckDuckGo und Mojeek werfen nach wenigen Abfragen eine Bot-Sperre. Die Wikipedia-API und
  direkte Seitenaufrufe sind verlässlich.
- Für Rechtsfragen gilt: Ein Begriff ist erst dann Gesetz, wenn du ihn im Gesetzestext
  findest. Bewährte Gegenprobe mit drei unabhängigen Quellen: Inhaltsverzeichnis des
  Gesetzes auf `gesetze-im-internet.de`, die dortige Normenliste, und `buzer.de`. Genau so
  wurde belegt, dass die **Verantwortungsgemeinschaft kein geltendes Recht ist**, sondern
  nur Eckpunkte vom 2. Februar 2024 existieren.

---

## 7 Subagenten

Sie sind nützlich für Audits, aber ihre Aussagen sind Rohmaterial, keine Befunde.

- **Ein Subagent hat einen Fehler frei erfunden**: „Frage 23 fehlt, die Liste springt von 22
  auf 24." Frage 23 existiert, die Liste ist lückenlos. Er zitierte außerdem eine Zeile
  2100 in einer Datei mit 1772 Zeilen.
- **Ein anderer meldete null Befunde für seinen Abschnitt** und zitierte dabei Zeilen weit
  außerhalb seines Bereichs, hatte den Abschnitt also gar nicht gelesen.
- **Prüfe jede Behauptung selbst nach**, bevor du sie dem Nutzer meldest oder umsetzt. Von
  sechs gemeldeten Befunden einer Runde waren vier echt und zwei falsch.
- Schreib in den Auftrag ausdrücklich hinein: **kein Formatierer**, und **keine Datei
  zurücksetzen, die der Subagent nicht selbst angelegt hat.**

---

## 8 Aufbau des Dokuments

Grobgliederung, damit du dich zurechtfindest, ohne die ganze Datei zu lesen:

| Teil                 | Inhalt                                                                    |
| -------------------- | ------------------------------------------------------------------------- |
| `## Worum es geht`   | Vom Nutzer geschrieben, unantastbar                                       |
| 1 bis 3              | Grundentscheidungen, Zusammenleben, Rechtsform und Syndikat               |
| **4**                | **Geld.** Raumbedarf, Standort, laufende Kosten, soziale Staffelung, Kapitalstock, Übersicht |
| 5 bis 7              | Weg dorthin, Gruppenaufbau, Governance                                    |
| 8                    | **Kinderschutz.** 8.0 bleibt unentschieden, Rest in Fassung A             |
| 9 bis 10             | Konflikt, Trennung, Flächen                                               |
| 11                   | Risikoregister, Nummern **1 bis 28**, lückenlos                           |
| 12                   | Offene Fragen, Nummern **1 bis 33**, lückenlos                            |
| 13 bis 14            | Nächste Schritte, Quellenverzeichnis (14.4) und Anlaufstellen             |
| A.1, A.2             | Anhänge                                                                    |
| Änderungshistorie    | Am Dateiende, jede Runde eine Zeile                                       |

**Vor dem Abschluss maschinell prüfen:** alle `(→ x.y)`-Verweise lösen auf, Risiken 1 bis 28
und Fragen 1 bis 33 ohne Lücke und ohne Dublette. Ein Prüfskript dafür lag zuletzt unter
`%TEMP%\wohnprojekt\pruef.py`.

---

## 9 Offene Punkte

Bereits gemeldet, keine Neuentdeckungen. Nicht als frische Befunde verkaufen.

- **Solidarbeitrag ans Mietshäuser Syndikat:** Die vertraglichen Sätze sind belegt (10 Cent
  je m² fest, dazu 0 bis 80 Cent stille Beteiligung, jährliche Steigerung um 0,5 Prozent
  der Jahresnettokaltmiete des Vorjahres). Offen bleiben die Praxis der Aussetzung und die
  Erwartung des Verbunds nach der Entschuldung. Beides steht in Frage 31.
- **Wiederbeschaffungswert einschließlich Bodenanteil**, Frage 19.
- **Wer während einer Auszeit nach 7.4 einzieht**, ungeklärt.
- **Fuchichos** bleibt `[ungeprüft]`, so vom Nutzer entschieden. Eine Suche am 26.08.2026
  fand keinerlei öffentliche Präsenz, der Kontakt läuft über den persönlichen Kreis.
- **Die Abschnitte 5 bis 9 wurden nie unabhängig Zeile für Zeile geprüft.** Wenn jemand
  behauptet, das Dokument sei vollständig auditiert, ist das falsch.

---

## 10 Umgangston

- **Kurz, direkt, ohne Füllwörter.** Keine Einleitungen, keine Zusammenfassungen des
  Offensichtlichen.
- **Eigene Fehler offen benennen.** Der Nutzer schätzt das ausdrücklich. In dieser Arbeit
  sind mehrere Aussagen des Agenten widerlegt worden, das Zugeben war jedes Mal der
  richtige Zug.
- **Nie Vollständigkeit behaupten ohne Beleg.** „Geprüft" heißt: Befehl gelaufen, Ausgabe
  gelesen, Ausgabe zitiert.
- Handeln statt vorschlagen. Wenn etwas zu entscheiden ist, frag konkret und kurz.

