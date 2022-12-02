
loaded = read("./day02.txt", String)
strategy = split(loaded, "\r\n")

scores = Dict(
    "A X" => 1 + 3,
    "B X" => 1 + 0,
    "C X" => 1 + 6,
    "A Y" => 2 + 6,
    "B Y" => 2 + 3,
    "C Y" => 2 + 0,
    "A Z" => 3 + 0,
    "B Z" => 3 + 6,
    "C Z" => 3 + 3,
)

function get_score(score_dict)
    score = 0
    for line in strategy
        score += score_dict[line]
    end
    return score
end

win_scores = Dict(
    "A X" => 3 + 0,
    "B X" => 1 + 0,
    "C X" => 2 + 0,
    "A Y" => 1 + 3,
    "B Y" => 2 + 3,
    "C Y" => 3 + 3,
    "A Z" => 2 + 6,
    "B Z" => 3 + 6,
    "C Z" => 1 + 6,
)

println(get_score(scores))
println(get_score(win_scores))
