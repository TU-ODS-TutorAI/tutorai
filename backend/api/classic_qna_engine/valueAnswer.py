#!/usr/bin/python3

from nltk import ngrams


def getBestAnswer(tokens, answers, sorted_idxs):
    token_amount = len(tokens)

    if(token_amount > 1):
        for idx in sorted_idxs:
            answer = cleanAnswer(answers[idx])
            matches = getMatches(tokens, answer)
            amount_matches = len(matches)
            if(amount_matches > 1):
                window_size = amount_matches * 4
                same_context = isSameContext(matches, answer, window_size)
                if(same_context == True):
                    solution = answers[sorted_idxs[idx]]
                    return solution
            else:
                solution_idx = getContextAnswer(tokens, answers, sorted_idxs)
                return answers[solution_idx]
    else:
        solution_idx = getContextAnswer(tokens, answers, sorted_idxs)
        return answers[solution_idx]


def cleanAnswer(answer):
    answer = answer.lower()
    answer = answer.replace("ä", "a")
    answer = answer.replace("ü", "u")
    answer = answer.replace("ö", "o")
    answer = answer.replace("-", "")

    return answer


def getMatches(tokens, answer):
    matches = []
    for token in tokens:
        if(token in answer):
            matches.append(token)

    return matches


def isSameContext(matches, answer, window):
    grams = ngrams(answer.split(), window)
    for gram in grams:
        if(set(matches).issubset(set(gram))):
            return True

    return False


def getContextAnswer(tokens, answers, sorted_idxs):
    lowest_tf_token = getLowestTf(tokens, answers)
    if not lowest_tf_token:
        return sorted_idxs[0]

    possible_solutions = []
    for idx in sorted_idxs:
            answer = cleanAnswer(answers[idx])
            if(lowest_tf_token in answer):
                possible_solutions.append((answer, idx))
    if(len(possible_solutions) == 1):
        return possible_solutions[0][1]
    else:
        best_score = 1
        for solution in possible_solutions:
            score = proximitySearch(solution[0], lowest_tf_token)
            if(score > best_score):
                best_score = score
                best_solution_idx = solution[1]

        if(best_score == 1):
            return sorted_idxs[0]
        else:
            return best_solution_idx


def getLowestTf(tokens, answers):
    tf_tokens = []
    for token in tokens:
        print(token)
        term_frequency = 0
        for answer in answers:
            answer = cleanAnswer(answer)
            if(token in answer):
                term_frequency += 1
        if(term_frequency != 0):
            tf_tokens.append((token, term_frequency))

    tf_tokens.sort(key=lambda x: x[1])
    if not tf_tokens:
        return tf_tokens
    else:
        return tf_tokens[0][0]


def proximitySearch(solution, token):

    return solution.count(token)

