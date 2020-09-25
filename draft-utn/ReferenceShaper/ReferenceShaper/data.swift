import Yams

let yamlDecoder = YAMLDecoder()

extension WrittenUnit {
    static let data: Data? = try? yamlDecoder.decode(Data.self, from: writtenUnitsYaml)
    struct Data: Decodable {
        subscript(writtenUnit: ReferenceShaper.WrittenUnit) -> WrittenUnit? {
            return ascii_transcription_to_written_unit[writtenUnit.rawValue] ?? nil
        }
        private let ascii_transcription_to_written_unit: [String: WrittenUnit?]
        internal init(from decoder: Decoder) throws {
            let container = try decoder.singleValueContainer()
            ascii_transcription_to_written_unit = (try? container.decode([String: WrittenUnit?].self)) ?? [:]
//            let written_unit_container = try container.
        }
        struct WrittenUnit: Decodable {
    //        let asciiTranscription: String
            let singleLetterTranscription: String?
            subscript(joiningForm: JoiningForm) -> Variant? {
                return joining_form_to_variant[joiningForm.rawValue]
            }
            private let joining_form_to_variant: [String: Variant]
            private enum CodingKeys: String, CodingKey {
                case singleLetterTranscription = "single_letter_transcription"
                case joining_form_to_variant
            }
            internal init(from decoder: Decoder) throws {
                let container = try decoder.container(keyedBy: CodingKeys.self)
                singleLetterTranscription = try? container.decode(String.self, forKey: .singleLetterTranscription)
                joining_form_to_variant = (try? container.decode([String: Variant].self, forKey: .joining_form_to_variant)) ?? [:]
            }
            struct Variant: Decodable {
                let representedLetters: Set<Character>
                let orthogonallyJoiningTypes: Set<OrthogonallyJoiningType>
                let note: String?
                private enum CodingKeys: String, CodingKey {
                    case representedLetters = "represented_phonetic_letters"
                    case orthogonallyJoiningTypes = "orthogonally_joining_types"
                    case note
                }
                internal init(from decoder: Decoder) throws {
                    let container = try decoder.container(keyedBy: CodingKeys.self)
                    if let r = try? container.decode([String: String].self, forKey: .representedLetters).keys {
                        representedLetters = Set(r.map { Character(rawValue: $0) ?? .unknown })
                    } else {
                        representedLetters = Set()
                    }
                    if let o = try? container.decode([String: String].self, forKey: .orthogonallyJoiningTypes).keys {
                        orthogonallyJoiningTypes = Set(o.map { OrthogonallyJoiningType(rawValue: $0) ?? .unknown })
                    } else {
                        orthogonallyJoiningTypes = Set()
                    }
                    note = try? container.decode(String.self, forKey: .note)
                }
            }
        }
    }
}

//extension Character {
//    static let data: [Character: Data?] = {
//        if let d = try? yamlDecoder.decode([Int: Data?].self, from: charactersYaml) {
//            return Dictionary(uniqueKeysWithValues: d.map { k, v in (Character(rawValue: v.asciiTranscription) ?? .unknown, v) })
//        } else {
//            return [:]
//        }
//    }()
//    struct Data: Decodable {
//        let asciiTranscription: String
//        let singleLetterTranscription: String?
//        let joiningFormToVariants: [JoiningForm: Set<Variant>]
//        private enum CodingKeys: String, CodingKey {
//            case asciiTranscription = "ascii_transcription"
//            case joiningFormToVariants = "joining_form_to_variants"
//        }
//        internal init(from decoder: Decoder) throws {
//            let data = try decoder.container(keyedBy: CodingKeys.self)
//        }
//        struct Variant: Decodable {
//        }
//    }
//}

let writtenUnitsYaml = """
--- # Mapping: ascii_transcription to written_unit

"A":
  joining_form_to_variant:
    isol: # A.isol
      represented_phonetic_letters: { "a", "e" }
    init: # A.init
      represented_phonetic_letters: { "aleph", "a", "e", "n" }
    medi: # A.medi
      represented_phonetic_letters: { "aleph", "a", "e", "n" }
      orthogonally_joining_types: { "trailing_minor" }
    fina: # A.fina
      represented_phonetic_letters: { "a", "e", "n" }
      orthogonally_joining_types: { "trailing_major" }

"Aa":
  single_letter_transcription: "Á"
  joining_form_to_variant:
    isol: # Aa.isol
      represented_phonetic_letters: { "a", "e" }
    fina: # Aa.fina
      represented_phonetic_letters: { "a" }

"I":
  joining_form_to_variant:
    isol: # I.isol
      represented_phonetic_letters: { "i", "j" }
    init: # I.init
      represented_phonetic_letters: { "i", "j", "y" }
    medi: # I.medi
      represented_phonetic_letters: { "i", "y" }
      orthogonally_joining_types: { "trailing_minor" }
    fina: # I.fina
      represented_phonetic_letters: { "i", "y" }
      orthogonally_joining_types: { "trailing_major" }

"Ii":
  single_letter_transcription: "Ị"
  joining_form_to_variant:
    isol: # Ii.isol
      represented_phonetic_letters: { "i" }
      note: "Early modern orthographies"
      typographical_decomposition: "I.isol + _dotbelow"

"O":
  joining_form_to_variant:
    init: # O.init
      represented_phonetic_letters: { "u", "ue" } # Particles
    medi: # O.medi
      represented_phonetic_letters: { "o", "u", "oe", "ue" }
      orthogonally_joining_types: { "trailing_major" }
    fina: # O.fina
      represented_phonetic_letters: { "o", "u", "oe", "ue"} # Marked, orthogonally joined
      orthogonally_joining_types: { "trailing_major" }

"Ue":
  single_letter_transcription: "Ü"
  joining_form_to_variant:
    fina: # Ue.fina
      represented_phonetic_letters: { "oe", "ue" }
      orthogonally_joining_types: { "trailing_major" }

"U":
  joining_form_to_variant:
    isol: # U.isol
      represented_phonetic_letters: { "u", "ue" }
    fina: # U.fina
      represented_phonetic_letters: { "o", "u", "oe", "ue", "w" }

"Uu":
  single_letter_transcription: "Ụ"
  joining_form_to_variant:
    isol: # Uu.isol
      represented_phonetic_letters: { "u", "ue" }
      note: "Early modern orthographies"
      typographical_decomposition: "U.isol + _dotbelow"

"N":
  joining_form_to_variant:
    init: # N.init
      represented_phonetic_letters: { "n" }
      typographical_decomposition: "A.init + _dotbelow"
    medi: # N.medi
      represented_phonetic_letters: { "n" }
      orthogonally_joining_types: { "trailing_minor" }
      typographical_decomposition: "A.medi + _dotbelow"
    fina: # N.fina
      represented_phonetic_letters: { "n" }
      typographical_decomposition: "A.fina + _dotbelow"

"B":
  joining_form_to_variant:
    init: # B.init
      represented_phonetic_letters: { "b" }
      orthogonally_joining_types: { "leading" }
    medi: # B.medi
      represented_phonetic_letters: { "b" }
      orthogonally_joining_types: { "leading" }
    fina: # B.fina
      represented_phonetic_letters: { "b" }

"P":
  joining_form_to_variant:
    init: # P.init
      represented_phonetic_letters: { "p" }
      orthogonally_joining_types: { "leading" }
    medi: # P.medi
      represented_phonetic_letters: { "p" }
      orthogonally_joining_types: { "leading" }
    fina: # P.fina
      represented_phonetic_letters: { "p" }

"H":
  joining_form_to_variant:
    init: # H.init
      represented_phonetic_letters: { "h" }
    medi: # H.medi
      represented_phonetic_letters: { "h", "g" }
      orthogonally_joining_types: { "trailing_minor" }
    fina: # H.fina
      represented_phonetic_letters: { "h", "g" }
      orthogonally_joining_types: { "trailing_minor" }

"Gh":
  single_letter_transcription: "Ğ"
  joining_form_to_variant:
    init: # Gh.init
      represented_phonetic_letters: { "g" }
    medi: # Gh.medi
      represented_phonetic_letters: { "g" }
      orthogonally_joining_types: { "trailing_minor" }
    fina: # Gh.fina
      represented_phonetic_letters: { "g" }
      orthogonally_joining_types: { "trailing_minor" }

"G":
  joining_form_to_variant:
    init: # G.init
      represented_phonetic_letters: { "h", "g" }
      orthogonally_joining_types: { "leading" }
    medi: # G.medi
      represented_phonetic_letters: { "h", "g" }
      orthogonally_joining_types: { "leading", "trailing_minor" }
    fina: # G.fina
      represented_phonetic_letters: { "g" }

"Gg":
  single_letter_transcription: "G̈"

"M":

"L":

"S":

"Sh":
  single_letter_transcription: "Ś"

"T":

"D":

"Dd":
  single_letter_transcription: "Đ"

"Ch":
  single_letter_transcription: "Ć"

"J":

"Y":

"R":

"W":
  joining_form_to_variant:
    init: # W.init
      represented_phonetic_letters: { "w" }
    medi: # W.medi
      represented_phonetic_letters: { "w", "ee" }
      orthogonally_joining_types: { "trailing_minor" }
    fina: # W.fina
      represented_phonetic_letters: { "w", "ee" }
      orthogonally_joining_types: { "trailing_minor" }

"F":

"K":

"C":

"Z":

"Hh":
  single_letter_transcription: "Ħ"

"Rh":
  single_letter_transcription: "Ř"

"Zr":
  single_letter_transcription: "Ž"

"Cr":
  single_letter_transcription: "Č"

...
"""

let charactersYaml = """
--- # Mapping: code_point to character

0x180E: # MONGOLIAN VOWEL SEPARATOR
  ascii_transcription: "MVS"

0x1807: # ᠇ MONGOLIAN SIBE SYLLABLE BOUNDARY MARKER
  ascii_transcription: "aleph"
  single_letter_transcription: "’"
  joining_form_to_variants:
    medi:
      "A": # aleph.medi.A

0x1820: # ᠠ MONGOLIAN LETTER A
  ascii_transcription: "a"
  joining_form_to_variants:
    isol:
      "A A": # a.isol.AA
        contextual_conditions: { "else" }
        fvs: 1
      "A": # a.isol.A
        contextual_conditions: { "particle" }
        fvs: 2
      "Aa": # a.isol.Aa
        contextual_conditions: { "chachlag" }
        fvs: 3
    init:
      "A A": # a.init.AA
        contextual_conditions: { "else" }
        fvs: 1
      "A": # a.init.A
        contextual_conditions: { "particle" }
        fvs: 2
    medi:
      "A": # a.medi.A
    fina:
      "A": # a.fina.A
      "Aa": # a.fina.Aa
        fvs: 1
        note: "Ali Gali a"

0x1821: # ᠡ MONGOLIAN LETTER E
  ascii_transcription: "e"
  joining_form_to_variants:
    isol:
      "A": # e.isol.A
        contextual_conditions: { "else" }
        fvs: 1
      "Aa": # e.isol.Aa
        contextual_conditions: { "chachlag" }
        fvs: 2
    init:
      "A": # e.init.A
    medi:
      "A": # e.medi.A
    fina:
      "A": # e.fina.A

0x1827: # ᠧ MONGOLIAN LETTER EE
  ascii_transcription: "ee"
  single_letter_transcription: "é"
  joining_form_to_variants:
    isol:
      "A W": # ee.isol.AW
    init:
      "A W": # ee.init.AW
    medi:
      "A": # ee.medi.W
    fina:
      "A": # ee.fina.W

0x1822: # ᠢ MONGOLIAN LETTER I
  ascii_transcription: "i"
  joining_form_to_variants:
    isol:
      "A I": # i.isol.AI
        contextual_conditions: { "else" }
        fvs: 1
      "I": # i.isol.I
        contextual_conditions: { "particle" }
        fvs: 2
      "Ii": # i.isol.Ii
        fvs: 3
        note: "Early modern orthographies"
    init:
      "A I": # i.init.AI
        contextual_conditions: { "else" }
        fvs: 1
      "I": # i.init.I
        contextual_conditions: { "particle" }
        fvs: 2
    medi:
      "I": # i.medi.I
        contextual_conditions: { "else" }
        fvs: 1
      "I I": # i.medi.II
        contextual_conditions: { "devsger" }
        fvs: 2
    fina:
      "I": # i.fina.I

0x1823: # ᠣ MONGOLIAN LETTER O
  ascii_transcription: "o"

0x1824: # ᠤ MONGOLIAN LETTER U
  ascii_transcription: "u"

0x1825: # ᠥ MONGOLIAN LETTER OE
  ascii_transcription: "oe"
  single_letter_transcription: "ö"

0x1826: # ᠦ MONGOLIAN LETTER UE
  ascii_transcription: "ue"
  single_letter_transcription: "ü"

0x1828: # ᠨ MONGOLIAN LETTER NA
  ascii_transcription: "n"

0x1829: # ᠩ MONGOLIAN LETTER ANG
  ascii_transcription: "ng"
  single_letter_transcription: "ŋ"

0x182A: # ᠪ MONGOLIAN LETTER BA
  ascii_transcription: "b"

0x182B: # ᠫ MONGOLIAN LETTER PA
  ascii_transcription: "p"

0x182C: # ᠬ MONGOLIAN LETTER QA
  ascii_transcription: "h"

0x182D: # ᠭ MONGOLIAN LETTER GA
  ascii_transcription: "g"

0x182E: # ᠮ MONGOLIAN LETTER MA
  ascii_transcription: "m"

0x182F: # ᠯ MONGOLIAN LETTER LA
  ascii_transcription: "l"

0x1830: # ᠰ MONGOLIAN LETTER SA
  ascii_transcription: "s"

0x1831: # ᠱ MONGOLIAN LETTER SHA
  ascii_transcription: "sh"
  single_letter_transcription: "ś"

0x1832: # ᠲ MONGOLIAN LETTER TA
  ascii_transcription: "t"

0x1833: # ᠳ MONGOLIAN LETTER DA
  ascii_transcription: "d"

0x1834: # ᠴ MONGOLIAN LETTER CHA
  ascii_transcription: "ch"
  single_letter_transcription: "ć"

0x1835: # ᠵ MONGOLIAN LETTER JA
  ascii_transcription: "j"

0x1836: # ᠶ MONGOLIAN LETTER YA
  ascii_transcription: "y"

0x1837: # ᠷ MONGOLIAN LETTER RA
  ascii_transcription: "r"

0x1838: # ᠸ MONGOLIAN LETTER WA
  ascii_transcription: "w"

0x1839: # ᠹ MONGOLIAN LETTER FA
  ascii_transcription: "f"

0x183B: # ᠻ MONGOLIAN LETTER KHA
  ascii_transcription: "k"

0x183C: # ᠼ MONGOLIAN LETTER TSA
  ascii_transcription: "c"

0x183D: # ᠽ MONGOLIAN LETTER ZA
  ascii_transcription: "z"

0x183E: # ᠾ MONGOLIAN LETTER HAA
  ascii_transcription: "hh"
  single_letter_transcription: "ħ"

0x183F: # ᠿ MONGOLIAN LETTER ZRA
  ascii_transcription: "rh"
  single_letter_transcription: "ř"

0x1840: # ᡀ MONGOLIAN LETTER LHA
  ascii_transcription: "lh"
  single_letter_transcription: "ł"

0x1841: # ᡁ MONGOLIAN LETTER ZHI
  ascii_transcription: "zr"
  single_letter_transcription: "ž"

0x1842: # ᡂ MONGOLIAN LETTER CHI
  ascii_transcription: "cr"
  single_letter_transcription: "č"

...
"""
