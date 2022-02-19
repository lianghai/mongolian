import Foundation

extension Unicode {
    typealias CodePoint = UInt32
    typealias Character = Scalar // Encoded character
    typealias GraphemeCluster = Swift.Character
}

enum JoiningForm: String, Decodable {
    case isol, `init`, medi, fina
    case unknown
}

enum OrthogonallyJoiningType: String, Decodable {
    case leading, trailing_major, trailing_minor
    case unknown
}

let jsonDecoder = JSONDecoder()
jsonDecoder.keyDecodingStrategy = .convertFromSnakeCase

enum WrittenUnit: String, CaseIterable, Decodable {
    case A, Aa, I, Ii, O, Ue, U, Uu,
         N, B, P, H, Gh, G, Gg, M, L, S, Sh, T, D, Dd, Ch, J, Y, R, W,
         F, K, C, Z, Hh, Rh, Zr, Cr
    case unknown
    var data: Data? { WrittenUnit.dataDict[self] }
}

enum Character: String, Decodable {
//    case MVS, FVS1, FVS2, FVS3
    case aleph
    case a, e, ee, i, o, u, oe, ue,
         n, ng, b, p, h, g, m, l, s, sh, t, d, ch, j, y, r, w,
         f, k, c, z, hh, rh, lh, zr, cr
    case unknown
    var data: Data? { Character.dataDict[self] }
    init?(codePoint: Unicode.CodePoint) {
        if let (char, _) = Character.dataDict.first(where: { _, data in data.codePoint == codePoint }) {
            self = char
        } else {
            return nil
        }
    }
    func resolveWrittenUnits(where joiningForm: JoiningForm, with condition: Condition) -> [WrittenUnit]? {
        return data?[joiningForm]?.first { $0.conditions?.contains(condition) ?? false }?.writtenUnits
    }
}

enum Condition: String, Decodable { // Contextual shaping condition
    case chachlag, particle, devsger
    case fallback
    case unknown
//    init(rawValue: Condition.RawValue) {
//        switch rawValue {
//        case "chachlag": self = .chachlag
//        case "particle": self = .particle
//        case "devsger": self = .devsger
//        case "fallback": self = .fallback
//        default: self = .unknown
//        }
//    }
}

typealias WrittenForm = (joiningForm: JoiningForm, writtenUnits: [WrittenUnit])

//dump(Character.a.applyCondition(.fallback, where: .isol) ?? [])

struct State {
    var joiningForm: JoiningForm?
    var condition: Condition?
}

let str = "ᠮᠣᠩᠭᠣᠯ"
//let str = "ᠠᠳᠠ"
var buffer = [(character: Character, state: State)]()
for char in str.unicodeScalars.map({ Character(codePoint: $0.value) ?? .unknown }) {
    buffer.append((char, State()))
}
for index in buffer.indices {
    buffer[index].state.joiningForm = .medi
}
for (char, state) in buffer {
    print(
        char.rawValue,
        state.joiningForm ?? "[joining form n/a]",
        state.condition ?? "[condition n/a]",
        state.joiningForm.flatMap { joiningForm in
            state.condition.flatMap { condition in
                char.resolveWrittenUnits(where: joiningForm, with: condition)
            }
        } ?? "[variant n/a]"
    )
}

//dump(WrittenUnit.A.data?[.medi])

//letter.joiningForm = .isol
//
//print(letter.joiningForm ?? "unknown")
//
//letter.applyCondition(.fallback)
//
//print(letter.writtenUnits ?? "unknown")

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
