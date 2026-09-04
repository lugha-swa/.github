# Lugha-swa

Shirika la programu za lugha ya Kiswahili, Afrika ya Mashariki.

## Swa — lugha ya kupanga ya Kiswahili

Swa ni lugha ya mifumo yenye sintaksia kamili ya Kiswahili. Hii si
tumizi ya lugha nyingine — ni mkusanyaji halisi unaojiandika wenyewe,
kutoka baiti za mkono hadi fixpoint.

### Kwa nini Swa ni mradi wenye nguvu

- **Kujikusanya kamili**: msomaji, mchanganuzi, mkaguzi, kiteremshi
  na kizalishe vyote vimeandikwa kwa Swa yenyewe. Mnyororo wa
  bootstrap unajifunga — `kwanza` (baiti 393 za mkono) hujenga
  `mbegu`, `mbegu` hujenga `stage1`, na `stage1` hujijenga hadi
  `stage2 == stage3` sawa kwa baiti. Hakuna gcc, ld, clang wala
  libc popote kwenye mnyororo wa uzalishaji.
- **Mfumo wa moduli halisi**: `husisha { maktaba/mfuatano.swa }`
  inatatuliwa na mkusanyaji wenyewe — tegemezi hufuatwa kwa mpito,
  marudio yanaondolewa, mzunguko unakataliwa kwa sauti. Maktaba ya
  kawaida ina rafu zake: `msingi/maktaba/` kwa msamiati
  (kumbukumbu, mfuatano, hesabu, orodha, ramani, mpangilio, faili,
  nasibu, wakati) na `msingi/mkusanyaji/` kwa mkusanyaji.
- **Uzingatiaji uliopimwa**: rekodi kamili
  (`hati/uthibitisho-wa-lugha.md`) inahesabu kila kipengele
  kilichojaribiwa kwenye minyororo yote miwili — kesi 467, kila moja
  ikikusanywa na kuendeshwa, si kusomwa. Kanuni ya mradi: program
  inakusanywa kwa usahihi AU inakataliwa kwa sauti. Jibu baya la
  kimya halikubaliki kamwe.
- **Majaribio ya kina**: mnyororo wa Swa pekee 304/304, fixpoint
  sawa kwa baiti kwenye kila ujenzi. Mbegu imegandishwa mara kumi
  na tatu, kila moja ikipitia lango kamili la majaribio kabla ya
  kugandishwa. Dereva wa zamani wa Rust/LLVM ni hazina ya
  kumbukumbu pekee (lugha-swa/swa-dereva) — hazina kuu ina lugha
  moja tu: Swa.
- **Maneno muhimu 13 pekee**: muundo, rudisha, kama, sivyo, wakati,
  kwa, fanya, vunja, endelea, chagua, hali, husisha, achilia.
  Kilichobaki ni maktaba — sawa na C, Go na Rust.
- **Faili asilia**: moduli ya faili inafanya kazi kwa syscalls
  moja kwa moja, bila libc. Kufungua, kusoma, kuandika, kufuta —
  zote asilia.

### Matoleo

- v0.0.1 — uzingatiaji wa lugha na rekodi iliyopimwa
- v0.0.2 — mfumo wa moduli: husisha ni kiungo halisi
- v0.0.3 — fanya (do-wakati), neno muhimu la 13

## Miradi

| Hazina | Maelezo |
|---|---|
| lugha-swa/swa | Mkusanyaji wa Swa — hazina kuu |
| lugha-swa.github.io | Tovuti rasmi ya lugha |
| lugha-swa/.github | Wasifu, kanuni, na violezo vya shirika |

## Kanuni

Kila mchango uko kwa Kiswahili. Mabadiliko huingia kupitia PR pekee.
Mbegu ni mzizi wa uaminifu — inajengwa na kujaribiwa KABLA ya
kugandishwa, hakuna ubaguzi.
