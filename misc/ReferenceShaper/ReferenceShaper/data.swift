extension WrittenUnit {
    static let dataDict: [WrittenUnit: Data] = {
        var dict = [WrittenUnit: Data]()
        try? jsonDecoder.decode([Data].self, from: writtenUnitsJson).forEach { data in
            if let writtenUnit = WrittenUnit(rawValue: data.asciiTranscription) {
                dict[writtenUnit] = data
            }
        }
        return dict
    }()
    struct Data: Decodable {
        let asciiTranscription: String
        let singleLetterTranscription: String?
        subscript(joiningForm: JoiningForm) -> Variant? {
            return joiningFormToVariant?[joiningForm.rawValue]
        }
        private let joiningFormToVariant: [String: Variant]?
        struct Variant: Decodable {
            let representedLetters: [Character]
            let orthogonallyJoiningTypes: [OrthogonallyJoiningType]?
            let note: String?
        }
    }
}

extension Character {
    static let dataDict: [Character: Data] = {
        var dict = [Character: Data]()
        try? jsonDecoder.decode([Data].self, from: charactersJson).forEach { data in
            if let char = Character(rawValue: data.asciiTranscription) {
                dict[char] = data
            }
        }
        return dict
    }()
    struct Data: Decodable {
        let codePoint: Unicode.CodePoint
        let asciiTranscription: String
        let singleLetterTranscription: String?
        subscript(joiningForm: JoiningForm) -> Set<Variant>? {
            return joiningFormToVariants?[joiningForm.rawValue].map { Set($0) }
        }
        private let joiningFormToVariants: [String: [Variant]]?
        struct Variant: Decodable, Hashable {
            let writtenUnits: [WrittenUnit]
            let conditions: [Condition]?
            let fvs: Int?
            let note: String?
        }
    }
}

let writtenUnitsJson = """
[{"ascii_transcription": "A", "joining_form_to_variant": {"isol": {"represented_letters": ["a", "e"]}, "init": {"represented_letters": ["aleph", "a", "e", "n"]}, "medi": {"represented_letters": ["aleph", "a", "e", "n"], "orthogonally_joining_types": ["trailing_minor"]}, "fina": {"represented_letters": ["a", "e", "n"], "orthogonally_joining_types": ["trailing_major"]}}}, {"ascii_transcription": "Aa", "single_letter_transcription": "Á", "joining_form_to_variant": {"isol": {"represented_letters": ["a", "e"]}, "fina": {"represented_letters": ["a"]}}}, {"ascii_transcription": "I", "joining_form_to_variant": {"isol": {"represented_letters": ["i", "j"]}, "init": {"represented_letters": ["i", "j", "y"]}, "medi": {"represented_letters": ["i", "y"], "orthogonally_joining_types": ["trailing_minor"]}, "fina": {"represented_letters": ["i", "y"], "orthogonally_joining_types": ["trailing_major"]}}}, {"ascii_transcription": "Ii", "single_letter_transcription": "Ị", "joining_form_to_variant": {"isol": {"represented_letters": ["i"], "note": "Early modern orthographies", "typographical_decomposition": "I.isol + _dotbelow"}}}, {"ascii_transcription": "O", "joining_form_to_variant": {"init": {"represented_letters": ["u", "ue"]}, "medi": {"represented_letters": ["o", "u", "oe", "ue"], "orthogonally_joining_types": ["trailing_major"]}, "fina": {"represented_letters": ["o", "u", "oe", "ue"], "orthogonally_joining_types": ["trailing_major"]}}}, {"ascii_transcription": "Ue", "single_letter_transcription": "Ü", "joining_form_to_variant": {"fina": {"represented_letters": ["oe", "ue"], "orthogonally_joining_types": ["trailing_major"]}}}, {"ascii_transcription": "U", "joining_form_to_variant": {"isol": {"represented_letters": ["u", "ue"]}, "fina": {"represented_letters": ["o", "u", "oe", "ue", "w"]}}}, {"ascii_transcription": "Uu", "single_letter_transcription": "Ụ", "joining_form_to_variant": {"isol": {"represented_letters": ["u", "ue"], "note": "Early modern orthographies", "typographical_decomposition": "U.isol + _dotbelow"}}}, {"ascii_transcription": "N", "joining_form_to_variant": {"init": {"represented_letters": ["n"], "typographical_decomposition": "A.init + _dotbelow"}, "medi": {"represented_letters": ["n"], "orthogonally_joining_types": ["trailing_minor"], "typographical_decomposition": "A.medi + _dotbelow"}, "fina": {"represented_letters": ["n"], "typographical_decomposition": "A.fina + _dotbelow"}}}, {"ascii_transcription": "B", "joining_form_to_variant": {"init": {"represented_letters": ["b"], "orthogonally_joining_types": ["leading"]}, "medi": {"represented_letters": ["b"], "orthogonally_joining_types": ["leading"]}, "fina": {"represented_letters": ["b"]}}}, {"ascii_transcription": "P", "joining_form_to_variant": {"init": {"represented_letters": ["p"], "orthogonally_joining_types": ["leading"]}, "medi": {"represented_letters": ["p"], "orthogonally_joining_types": ["leading"]}, "fina": {"represented_letters": ["p"]}}}, {"ascii_transcription": "H", "joining_form_to_variant": {"init": {"represented_letters": ["h"]}, "medi": {"represented_letters": ["h", "g"], "orthogonally_joining_types": ["trailing_minor"]}, "fina": {"represented_letters": ["h", "g"], "orthogonally_joining_types": ["trailing_minor"]}}}, {"ascii_transcription": "Gh", "single_letter_transcription": "Ğ", "joining_form_to_variant": {"init": {"represented_letters": ["g"]}, "medi": {"represented_letters": ["g"], "orthogonally_joining_types": ["trailing_minor"]}, "fina": {"represented_letters": ["g"], "orthogonally_joining_types": ["trailing_minor"]}}}, {"ascii_transcription": "G", "joining_form_to_variant": {"init": {"represented_letters": ["h", "g"], "orthogonally_joining_types": ["leading"]}, "medi": {"represented_letters": ["h", "g"], "orthogonally_joining_types": ["leading", "trailing_minor"]}, "fina": {"represented_letters": ["g"]}}}, {"ascii_transcription": "Gg", "single_letter_transcription": "G̈"}, {"ascii_transcription": "M"}, {"ascii_transcription": "L"}, {"ascii_transcription": "S"}, {"ascii_transcription": "Sh", "single_letter_transcription": "Ś"}, {"ascii_transcription": "T"}, {"ascii_transcription": "D"}, {"ascii_transcription": "Dd", "single_letter_transcription": "Đ"}, {"ascii_transcription": "Ch", "single_letter_transcription": "Ć"}, {"ascii_transcription": "J"}, {"ascii_transcription": "Y"}, {"ascii_transcription": "R"}, {"ascii_transcription": "W", "joining_form_to_variant": {"init": {"represented_letters": ["w"]}, "medi": {"represented_letters": ["w", "ee"], "orthogonally_joining_types": ["trailing_minor"]}, "fina": {"represented_letters": ["w", "ee"], "orthogonally_joining_types": ["trailing_minor"]}}}, {"ascii_transcription": "F"}, {"ascii_transcription": "K"}, {"ascii_transcription": "C"}, {"ascii_transcription": "Z"}, {"ascii_transcription": "Hh", "single_letter_transcription": "Ħ"}, {"ascii_transcription": "Rh", "single_letter_transcription": "Ř"}, {"ascii_transcription": "Zr", "single_letter_transcription": "Ž"}, {"ascii_transcription": "Cr", "single_letter_transcription": "Č"}]
""".data(using: .utf8)!

let charactersJson = """
[{"code_point": 6158, "ascii_transcription": "MVS"}, {"code_point": 6151, "ascii_transcription": "aleph", "single_letter_transcription": "’", "joining_form_to_variants": {"medi": [{"written_units": ["A"]}]}}, {"code_point": 6176, "ascii_transcription": "a", "joining_form_to_variants": {"isol": [{"written_units": ["A", "A"], "conditions": ["fallback"], "fvs": 1, "known_fvs_usage": []}, {"written_units": ["A"], "fvs": 3, "known_fvs_usage": ["exclamatory particle: a A"]}, {"written_units": ["Aa"], "conditions": ["chachlag"], "fvs": 2, "known_fvs_usage": []}], "init": [{"written_units": ["A", "A"], "conditions": ["fallback"], "fvs": 1}, {"written_units": ["A"], "conditions": ["particle"], "fvs": 2}], "medi": [{"written_units": ["A"]}], "fina": [{"written_units": ["A"]}, {"written_units": ["Aa"], "fvs": 1, "known_fvs_usage": ["Ali Gali, na NÁ"], "note": "Ali Gali a"}]}}, {"code_point": 6177, "ascii_transcription": "e", "joining_form_to_variants": {"isol": [{"written_units": ["A"], "conditions": ["fallback"], "fvs": 1}, {"written_units": ["Aa"], "conditions": ["chachlag"], "fvs": 2}], "init": [{"written_units": ["A"]}], "medi": [{"written_units": ["A"]}], "fina": [{"written_units": ["A"]}]}}, {"code_point": 6183, "ascii_transcription": "ee", "single_letter_transcription": "é", "joining_form_to_variants": {"isol": [{"written_units": ["A", "W"]}], "init": [{"written_units": ["A", "W"]}], "medi": [{"written_units": ["A"]}], "fina": [{"written_units": ["A"]}]}}, {"code_point": 6178, "ascii_transcription": "i", "joining_form_to_variants": {"isol": [{"written_units": ["A", "I"], "conditions": ["fallback"], "fvs": 1}, {"written_units": ["I"], "conditions": ["particle"], "fvs": 2}, {"written_units": ["Ii"], "fvs": 3, "note": "Early modern orthographies"}], "init": [{"written_units": ["A", "I"], "conditions": ["fallback"], "fvs": 1}, {"written_units": ["I"], "conditions": ["particle"], "fvs": 2}], "medi": [{"written_units": ["I"], "conditions": ["fallback"], "fvs": 1}, {"written_units": ["I", "I"], "conditions": ["devsger"], "fvs": 2}], "fina": [{"written_units": ["I"]}]}}, {"code_point": 6179, "ascii_transcription": "o"}, {"code_point": 6180, "ascii_transcription": "u"}, {"code_point": 6181, "ascii_transcription": "oe", "single_letter_transcription": "ö"}, {"code_point": 6182, "ascii_transcription": "ue", "single_letter_transcription": "ü"}, {"code_point": 6184, "ascii_transcription": "n"}, {"code_point": 6185, "ascii_transcription": "ng", "single_letter_transcription": "ŋ"}, {"code_point": 6186, "ascii_transcription": "b"}, {"code_point": 6187, "ascii_transcription": "p"}, {"code_point": 6188, "ascii_transcription": "h"}, {"code_point": 6189, "ascii_transcription": "g"}, {"code_point": 6190, "ascii_transcription": "m"}, {"code_point": 6191, "ascii_transcription": "l"}, {"code_point": 6192, "ascii_transcription": "s"}, {"code_point": 6193, "ascii_transcription": "sh", "single_letter_transcription": "ś"}, {"code_point": 6194, "ascii_transcription": "t"}, {"code_point": 6195, "ascii_transcription": "d"}, {"code_point": 6196, "ascii_transcription": "ch", "single_letter_transcription": "ć"}, {"code_point": 6197, "ascii_transcription": "j"}, {"code_point": 6198, "ascii_transcription": "y"}, {"code_point": 6199, "ascii_transcription": "r"}, {"code_point": 6200, "ascii_transcription": "w"}, {"code_point": 6201, "ascii_transcription": "f"}, {"code_point": 6203, "ascii_transcription": "k"}, {"code_point": 6204, "ascii_transcription": "c"}, {"code_point": 6205, "ascii_transcription": "z"}, {"code_point": 6206, "ascii_transcription": "hh", "single_letter_transcription": "ħ"}, {"code_point": 6207, "ascii_transcription": "rh", "single_letter_transcription": "ř"}, {"code_point": 6208, "ascii_transcription": "lh", "single_letter_transcription": "ł"}, {"code_point": 6209, "ascii_transcription": "zr", "single_letter_transcription": "ž"}, {"code_point": 6210, "ascii_transcription": "cr", "single_letter_transcription": "č"}]
""".data(using: .utf8)!
