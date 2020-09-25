import Foundation

extension WrittenUnit {
    static let dataDictionary: [WrittenUnit: Data] = {
        let dict = (try? jsonDecoder.decode([String: Data].self, from: writtenUnitsJson)) ?? [:]
        return Dictionary(uniqueKeysWithValues: dict.map { k, v in (WrittenUnit(rawValue: k) ?? .unknown, v) })
    }()
//    struct Data: Decodable {
//        subscript(writtenUnit: ReferenceShaper.WrittenUnit) -> WrittenUnit? {
//            return ascii_transcription_to_written_unit[writtenUnit.rawValue] ?? nil
//        }
//        private let ascii_transcription_to_written_unit: [String: WrittenUnit?]
//        internal init(from decoder: Decoder) throws {
//            let container = try decoder.singleValueContainer()
//            ascii_transcription_to_written_unit = (try? container.decode([String: WrittenUnit?].self)) ?? [:]
////            let written_unit_container = try container.
//        }
//        struct WrittenUnit: Decodable {
//    //        let asciiTranscription: String
//            let singleLetterTranscription: String?
//            subscript(joiningForm: JoiningForm) -> Variant? {
//                return joining_form_to_variant[joiningForm.rawValue]
//            }
//            private let joining_form_to_variant: [String: Variant]
//            private enum CodingKeys: String, CodingKey {
//                case singleLetterTranscription = "single_letter_transcription"
//                case joining_form_to_variant
//            }
//            internal init(from decoder: Decoder) throws {
//                let container = try decoder.container(keyedBy: CodingKeys.self)
//                singleLetterTranscription = try? container.decode(String.self, forKey: .singleLetterTranscription)
//                joining_form_to_variant = (try? container.decode([String: Variant].self, forKey: .joining_form_to_variant)) ?? [:]
//            }
//            struct Variant: Decodable {
//                let representedLetters: Set<Character>
//                let orthogonallyJoiningTypes: Set<OrthogonallyJoiningType>
//                let note: String?
//                private enum CodingKeys: String, CodingKey {
//                    case representedLetters = "represented_phonetic_letters"
//                    case orthogonallyJoiningTypes = "orthogonally_joining_types"
//                    case note
//                }
//                internal init(from decoder: Decoder) throws {
//                    let container = try decoder.container(keyedBy: CodingKeys.self)
//                    if let r = try? container.decode([String: String].self, forKey: .representedLetters).keys {
//                        representedLetters = Set(r.map { Character(rawValue: $0) ?? .unknown })
//                    } else {
//                        representedLetters = Set()
//                    }
//                    if let o = try? container.decode([String: String].self, forKey: .orthogonallyJoiningTypes).keys {
//                        orthogonallyJoiningTypes = Set(o.map { OrthogonallyJoiningType(rawValue: $0) ?? .unknown })
//                    } else {
//                        orthogonallyJoiningTypes = Set()
//                    }
//                    note = try? container.decode(String.self, forKey: .note)
//                }
//            }
//        }
//    }
}

extension Character {
    static let dataDictionary: [Character: Data] = {
        var result = [Character: Data]()
        if let dict = try? jsonDecoder.decode([Int: Data].self, from: charactersJson) {
            for data in dict.values {
                if let char = Character(rawValue: data.asciiTranscription) {
                    result[char] = data
                }
            }
        }
        return result
    }()
    struct Data: Decodable {
        let asciiTranscription: String
        let singleLetterTranscription: String?
        private let joiningFormToVariants: [JoiningForm: Set<Variant>]
        subscript(joiningForm: JoiningForm) -> Set<Variant> {
            return joiningFormToVariants[joiningForm] ?? Set()
        }
        enum CodingKeys: String, CodingKey {
            case asciiTranscription, singleLetterTranscription
            case joiningFormToVariants
        }
//        enum JoiningFormToVariantsCodingKeys: String, CaseIterable, CodingKey {
//            case isol, `init`, medi, fina
//        }
//        enum VariantCodingKeys: String, CodingKey {
//            case isol, `init`, medi, fina
//        }
        init(from decoder: Decoder) throws {
            let container = try decoder.container(keyedBy: CodingKeys.self)
            asciiTranscription = try container.decode(String.self, forKey: .asciiTranscription)
            singleLetterTranscription = try? container.decode(String?.self, forKey: .singleLetterTranscription)
//            let dict = try? container.decode([String: [String: Variant]].self, forKey: .joiningFormToVariants)
            var joiningFormToVariantsContainer = try container.nestedUnkeyedContainer(forKey: .joiningFormToVariants)
            dump(try joiningFormToVariantsContainer.nestedUnkeyedContainer())
//            let array = joiningFormToVariantsContainer.decode([String: [String: Variant]].self)
//            for key in JoiningFormToVariantsCodingKeys.allCases {
//                let container = joiningFormToVariantsContainer.nestedContainer(keyedBy: <#T##CodingKey.Protocol#>, forKey: <#T##KeyedDecodingContainer<JoiningFormToVariantsCodingKeys>.Key#>)
//            }
            joiningFormToVariants = [:]
        }
        struct Variant: Decodable, Hashable {
//            let writtenUnits: [WrittenUnit]
            let contextualConditions: Set<Condition>
            let fvs: Int?
            let note: String?
        }
    }
}

let writtenUnitsJson = """
[{"ascii_transcription": "A", "joining_form_to_variant": {"isol": {"represented_phonetic_letters": ["a", "e"]}, "init": {"represented_phonetic_letters": ["aleph", "a", "e", "n"]}, "medi": {"represented_phonetic_letters": ["aleph", "a", "e", "n"], "orthogonally_joining_types": ["trailing_minor"]}, "fina": {"represented_phonetic_letters": ["a", "e", "n"], "orthogonally_joining_types": ["trailing_major"]}}}, {"ascii_transcription": "Aa", "single_letter_transcription": "Á", "joining_form_to_variant": {"isol": {"represented_phonetic_letters": ["a", "e"]}, "fina": {"represented_phonetic_letters": ["a"]}}}, {"ascii_transcription": "I", "joining_form_to_variant": {"isol": {"represented_phonetic_letters": ["i", "j"]}, "init": {"represented_phonetic_letters": ["i", "j", "y"]}, "medi": {"represented_phonetic_letters": ["i", "y"], "orthogonally_joining_types": ["trailing_minor"]}, "fina": {"represented_phonetic_letters": ["i", "y"], "orthogonally_joining_types": ["trailing_major"]}}}, {"ascii_transcription": "Ii", "single_letter_transcription": "Ị", "joining_form_to_variant": {"isol": {"represented_phonetic_letters": ["i"], "note": "Early modern orthographies", "typographical_decomposition": "I.isol + _dotbelow"}}}, {"ascii_transcription": "O", "joining_form_to_variant": {"init": {"represented_phonetic_letters": ["u", "ue"]}, "medi": {"represented_phonetic_letters": ["o", "u", "oe", "ue"], "orthogonally_joining_types": ["trailing_major"]}, "fina": {"represented_phonetic_letters": ["o", "u", "oe", "ue"], "orthogonally_joining_types": ["trailing_major"]}}}, {"ascii_transcription": "Ue", "single_letter_transcription": "Ü", "joining_form_to_variant": {"fina": {"represented_phonetic_letters": ["oe", "ue"], "orthogonally_joining_types": ["trailing_major"]}}}, {"ascii_transcription": "U", "joining_form_to_variant": {"isol": {"represented_phonetic_letters": ["u", "ue"]}, "fina": {"represented_phonetic_letters": ["o", "u", "oe", "ue", "w"]}}}, {"ascii_transcription": "Uu", "single_letter_transcription": "Ụ", "joining_form_to_variant": {"isol": {"represented_phonetic_letters": ["u", "ue"], "note": "Early modern orthographies", "typographical_decomposition": "U.isol + _dotbelow"}}}, {"ascii_transcription": "N", "joining_form_to_variant": {"init": {"represented_phonetic_letters": ["n"], "typographical_decomposition": "A.init + _dotbelow"}, "medi": {"represented_phonetic_letters": ["n"], "orthogonally_joining_types": ["trailing_minor"], "typographical_decomposition": "A.medi + _dotbelow"}, "fina": {"represented_phonetic_letters": ["n"], "typographical_decomposition": "A.fina + _dotbelow"}}}, {"ascii_transcription": "B", "joining_form_to_variant": {"init": {"represented_phonetic_letters": ["b"], "orthogonally_joining_types": ["leading"]}, "medi": {"represented_phonetic_letters": ["b"], "orthogonally_joining_types": ["leading"]}, "fina": {"represented_phonetic_letters": ["b"]}}}, {"ascii_transcription": "P", "joining_form_to_variant": {"init": {"represented_phonetic_letters": ["p"], "orthogonally_joining_types": ["leading"]}, "medi": {"represented_phonetic_letters": ["p"], "orthogonally_joining_types": ["leading"]}, "fina": {"represented_phonetic_letters": ["p"]}}}, {"ascii_transcription": "H", "joining_form_to_variant": {"init": {"represented_phonetic_letters": ["h"]}, "medi": {"represented_phonetic_letters": ["h", "g"], "orthogonally_joining_types": ["trailing_minor"]}, "fina": {"represented_phonetic_letters": ["h", "g"], "orthogonally_joining_types": ["trailing_minor"]}}}, {"ascii_transcription": "Gh", "single_letter_transcription": "Ğ", "joining_form_to_variant": {"init": {"represented_phonetic_letters": ["g"]}, "medi": {"represented_phonetic_letters": ["g"], "orthogonally_joining_types": ["trailing_minor"]}, "fina": {"represented_phonetic_letters": ["g"], "orthogonally_joining_types": ["trailing_minor"]}}}, {"ascii_transcription": "G", "joining_form_to_variant": {"init": {"represented_phonetic_letters": ["h", "g"], "orthogonally_joining_types": ["leading"]}, "medi": {"represented_phonetic_letters": ["h", "g"], "orthogonally_joining_types": ["leading", "trailing_minor"]}, "fina": {"represented_phonetic_letters": ["g"]}}}, {"ascii_transcription": "Gg", "single_letter_transcription": "G̈"}, {"ascii_transcription": "M"}, {"ascii_transcription": "L"}, {"ascii_transcription": "S"}, {"ascii_transcription": "Sh", "single_letter_transcription": "Ś"}, {"ascii_transcription": "T"}, {"ascii_transcription": "D"}, {"ascii_transcription": "Dd", "single_letter_transcription": "Đ"}, {"ascii_transcription": "Ch", "single_letter_transcription": "Ć"}, {"ascii_transcription": "J"}, {"ascii_transcription": "Y"}, {"ascii_transcription": "R"}, {"ascii_transcription": "W", "joining_form_to_variant": {"init": {"represented_phonetic_letters": ["w"]}, "medi": {"represented_phonetic_letters": ["w", "ee"], "orthogonally_joining_types": ["trailing_minor"]}, "fina": {"represented_phonetic_letters": ["w", "ee"], "orthogonally_joining_types": ["trailing_minor"]}}}, {"ascii_transcription": "F"}, {"ascii_transcription": "K"}, {"ascii_transcription": "C"}, {"ascii_transcription": "Z"}, {"ascii_transcription": "Hh", "single_letter_transcription": "Ħ"}, {"ascii_transcription": "Rh", "single_letter_transcription": "Ř"}, {"ascii_transcription": "Zr", "single_letter_transcription": "Ž"}, {"ascii_transcription": "Cr", "single_letter_transcription": "Č"}]
""".data(using: .utf8)!

let charactersJson = """
[{"code_point": 6158, "ascii_transcription": "MVS"}, {"code_point": 6151, "ascii_transcription": "aleph", "single_letter_transcription": "’", "joining_form_to_variants": {"medi": [{"written_units": ["A"]}]}}, {"code_point": 6176, "ascii_transcription": "a", "joining_form_to_variants": {"isol": [{"written_units": ["A", "A"], "contextual_conditions": ["else"], "fvs": 1}, {"written_units": ["A"], "contextual_conditions": ["particle"], "fvs": 2}, {"written_units": ["Aa"], "contextual_conditions": ["chachlag"], "fvs": 3}], "init": [{"written_units": ["A", "A"], "contextual_conditions": ["else"], "fvs": 1}, {"written_units": ["A"], "contextual_conditions": ["particle"], "fvs": 2}], "medi": [{"written_units": ["A"]}], "fina": [{"written_units": ["A"]}, {"written_units": ["Aa"], "fvs": 1, "note": "Ali Gali a"}]}}, {"code_point": 6177, "ascii_transcription": "e", "joining_form_to_variants": {"isol": [{"written_units": ["A"], "contextual_conditions": ["else"], "fvs": 1}, {"written_units": ["Aa"], "contextual_conditions": ["chachlag"], "fvs": 2}], "init": [{"written_units": ["A"]}], "medi": [{"written_units": ["A"]}], "fina": [{"written_units": ["A"]}]}}, {"code_point": 6183, "ascii_transcription": "ee", "single_letter_transcription": "é", "joining_form_to_variants": {"isol": [{"written_units": ["A", "W"]}], "init": [{"written_units": ["A", "W"]}], "medi": [{"written_units": ["A"]}], "fina": [{"written_units": ["A"]}]}}, {"code_point": 6178, "ascii_transcription": "i", "joining_form_to_variants": {"isol": [{"written_units": ["A", "I"], "contextual_conditions": ["else"], "fvs": 1}, {"written_units": ["I"], "contextual_conditions": ["particle"], "fvs": 2}, {"written_units": ["Ii"], "fvs": 3, "note": "Early modern orthographies"}], "init": [{"written_units": ["A", "I"], "contextual_conditions": ["else"], "fvs": 1}, {"written_units": ["I"], "contextual_conditions": ["particle"], "fvs": 2}], "medi": [{"written_units": ["I"], "contextual_conditions": ["else"], "fvs": 1}, {"written_units": ["I", "I"], "contextual_conditions": ["devsger"], "fvs": 2}], "fina": [{"written_units": ["I"]}]}}, {"code_point": 6179, "ascii_transcription": "o"}, {"code_point": 6180, "ascii_transcription": "u"}, {"code_point": 6181, "ascii_transcription": "oe", "single_letter_transcription": "ö"}, {"code_point": 6182, "ascii_transcription": "ue", "single_letter_transcription": "ü"}, {"code_point": 6184, "ascii_transcription": "n"}, {"code_point": 6185, "ascii_transcription": "ng", "single_letter_transcription": "ŋ"}, {"code_point": 6186, "ascii_transcription": "b"}, {"code_point": 6187, "ascii_transcription": "p"}, {"code_point": 6188, "ascii_transcription": "h"}, {"code_point": 6189, "ascii_transcription": "g"}, {"code_point": 6190, "ascii_transcription": "m"}, {"code_point": 6191, "ascii_transcription": "l"}, {"code_point": 6192, "ascii_transcription": "s"}, {"code_point": 6193, "ascii_transcription": "sh", "single_letter_transcription": "ś"}, {"code_point": 6194, "ascii_transcription": "t"}, {"code_point": 6195, "ascii_transcription": "d"}, {"code_point": 6196, "ascii_transcription": "ch", "single_letter_transcription": "ć"}, {"code_point": 6197, "ascii_transcription": "j"}, {"code_point": 6198, "ascii_transcription": "y"}, {"code_point": 6199, "ascii_transcription": "r"}, {"code_point": 6200, "ascii_transcription": "w"}, {"code_point": 6201, "ascii_transcription": "f"}, {"code_point": 6203, "ascii_transcription": "k"}, {"code_point": 6204, "ascii_transcription": "c"}, {"code_point": 6205, "ascii_transcription": "z"}, {"code_point": 6206, "ascii_transcription": "hh", "single_letter_transcription": "ħ"}, {"code_point": 6207, "ascii_transcription": "rh", "single_letter_transcription": "ř"}, {"code_point": 6208, "ascii_transcription": "lh", "single_letter_transcription": "ł"}, {"code_point": 6209, "ascii_transcription": "zr", "single_letter_transcription": "ž"}, {"code_point": 6210, "ascii_transcription": "cr", "single_letter_transcription": "č"}]
""".data(using: .utf8)!
