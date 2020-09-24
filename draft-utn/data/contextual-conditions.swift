struct Letter {
    var identifier: str
    var written_form: ()
    func applyCondition(_ Condition) {
        written_form = variants[cursive_position][condition]
    }
}

enum Condition {
    case fallback
    case chachlag
}

func resolveCondition(for letter: Letter, in context: Context) -> Condition {
    
    var condition = .fallback
    
    // Chachlag
    if  [.a, .e].contains(letter), context.before.hasSuffix(.mvs) {
        condition = .chachlag
    }
    
    // Syllabic
    switch letter {
    case .o, .u, .oe, .ue:
        if context.before {
            condition = .marked
        }
    case .n, .j, .y, .w:
        if context.after {
            condition = .chachlag_onset
        }
    case .h, .g:
        if context.after {
            condition = .chachlag_onset
        }
    case .n, .d:
        if context.after {
            condition = .onset
        } else if context.before {
            condition = .devsger
        }
    case .h, .g:
        if context.after {
            condition = .masculine_onset
        } else if context.after {
            condition = .feminine
        }
    case .g:
        if context.before {
            condition = .masculine_devsger
        } else if context.before {
            condition = .feminine
        } else if context.before {
            condition = .masculine_devsger
        } else {
            condition = .feminine
        }
    default:
        break
    }
    
    // Particle
    switch letter {
    case .a, .i, .u, .ue, .d:
        if context.before == .nnbsp {
            condition = .particle
        }
    case .u, .ue:
        if context.before {
            condition = .particle
        }
    case .y:
        if context.before, context.after {
            condition = .particle
        }
    default:
        break
    }
    
    // Devsger i
    switch letter {
    case .i:
        if context.before {
            condition = .devsger
        }
    default:
        break
    }
    
    // Post-bowed
    if [.o, .u, .oe, .ue].contains(letter), written_form == .U, context.before {
        condition = .post_bowed
    }
    
    return condition
}
