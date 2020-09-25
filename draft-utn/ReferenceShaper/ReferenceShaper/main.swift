import Foundation

extension Unicode {
    typealias CodePoint = UInt32
    typealias Character = Scalar // Encoded character
    typealias GraphemeCluster = Swift.Character
}

enum JoiningForm: String {
    case isol, `init`, medi, fina
    case unknown
}

enum OrthogonallyJoiningType: String {
    case leading, trailing_major, trailing_minor
    case unknown
}

let jsonDecoder = JSONDecoder()
jsonDecoder.keyDecodingStrategy = .convertFromSnakeCase

enum WrittenUnit: String {
    case A, Aa, I, Ii, O, Ue, U, Uu,
         N, B, P, H, Gh, G, Gg, M, L, S, Sh, T, D, Dd, Ch, J, Y, R, W,
         F, K, C, Z, Hh, Rh, Zr, Cr
    case unknown
    var data: Data? {
        return WrittenUnit.dataDictionary[self]
    }
}

//dump(WrittenUnit.B.data?[.medi])

typealias Variant = (joiningForm: JoiningForm, writtenUnits: [WrittenUnit])

enum Character: String {
//    case MVS, FVS1, FVS2, FVS3
    case aleph
    case a, e, ee, i, o, u, oe, ue,
         n, ng, b, p, h, g, m, l, s, sh, t, d, ch, j, y, r, w,
         f, k, c, z, hh, rh, lh, zr, cr
    case unknown
    var data: Data? {
        return Character.dataDictionary[self]
    }
}

dump(Character.a.data)

enum Condition: String, Decodable { // Contextual shaping condition
    case fallback
    case chachlag, particle
    case unknown
}

//static let data: [Character: [JoiningForm: [[WrittenUnit]: Set<Condition>]]] = [
//    .a: [
//        .isol: [
//            [.A, .A]: [.fallback]
//        ]
//    ]
//]
//lazy var conditionToWrittenUnits: [Condition: [WrittenUnit]]? = {
//    var conditionToWrittenUnits: [Condition: [WrittenUnit]] = [:]
//    if let joiningForm = joiningForm, let writtenUnitsToConditions = Letter.data[codePoint]?[joiningForm] {
//        for (writtenUnits, conditions) in writtenUnitsToConditions {
//            for condition in conditions {
//                conditionToWrittenUnits[condition] = writtenUnits
//            }
//        }
//    }
//    return conditionToWrittenUnits
//}()
//

//struct Element { // Phonetic letter
//
//    let character: Character
//    var joiningForm: JoiningForm?
//    var writtenUnits: [WrittenUnit]?
//
//    init?(codePoint: Unicode.CodePoint) {
//        guard let character = Character(rawValue: codePoint) else {
//            return nil
//        }
//        self.character = character
//    }
//    mutating func applyCondition(_ condition: Condition) {
//        writtenUnits = conditionToWrittenUnits?[condition]
//    }
//}

//for character in Character.allCases {
//    print(String(Unicode.Scalar(character.rawValue)!))
//    print(String(character.rawValue, radix: 16, uppercase: true))
//}

//var letters = "ᠮᠣᠩᠭᠣᠯ".unicodeScalars.compactMap { Letter(codePoint: $0.value) }
//
//var letter = letters[0]
//
//print(letter.character.rawValue)
//
//letter.joiningForm = .isol
//
//print(letter.joiningForm ?? "unknown")
//
//letter.applyCondition(.fallback)
//
//print(letter.writtenUnits ?? "unknown")
//
//struct Context {
//    let before: [Letter]
//    let after: [Letter]
//}

//func resolveVariant(for letter: Letter, in context: Context) -> Variant {
//
//    var condition = Condition.fallback
//
//    // Chachlag
//    if  [.a, .e].contains(letter), context.before.hasSuffix(.MVS) {
//        condition = .chachlag
//    }
//
//    // Syllabic
//    switch letter {
//    case .o, .u, .oe, .ue:
//        if context.before {
//            condition = .marked
//        }
//    case .n, .j, .y, .w:
//        if context.after {
//            condition = .chachlag_onset
//        }
//    case .h, .g:
//        if context.after {
//            condition = .chachlag_onset
//        }
//    case .n, .d:
//        if context.after {
//            condition = .onset
//        } else if context.before {
//            condition = .devsger
//        }
//    case .h, .g:
//        if context.after {
//            condition = .masculine_onset
//        } else if context.after {
//            condition = .feminine
//        }
//    case .g:
//        if context.before {
//            condition = .masculine_devsger
//        } else if context.before {
//            condition = .feminine
//        } else if context.before {
//            condition = .masculine_devsger
//        } else {
//            condition = .feminine
//        }
//    default:
//        break
//    }
//
//    // Particle
//    switch letter {
//    case .a, .i, .u, .ue, .d:
//        if context.before == .nnbsp {
//            condition = .particle
//        }
//    case .u, .ue:
//        if context.before {
//            condition = .particle
//        }
//    case .y:
//        if context.before, context.after {
//            condition = .particle
//        }
//    default:
//        break
//    }
//
//    // Devsger i
//    switch letter {
//    case .i:
//        if context.before {
//            condition = .devsger
//        }
//    default:
//        break
//    }
//
//    // Post-bowed
//    if [.o, .u, .oe, .ue].contains(letter), written_form == .U, context.before {
//        condition = .post_bowed
//    }
//
//    return condition
//}
