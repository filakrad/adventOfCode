
loaded = read("./day03.txt", String)
lines = split(loaded, "\r\n")

first_lower_char = Int('a')
first_upper_char = Int('A')

function get_score(score_char)
    if islowercase(score_char)
        return Int(score_char) - first_lower_char + 1
    else
        return Int(score_char) - first_upper_char + 27
    end
end


function star01()
    score = 0
    for line in lines
        midpoint = Int(length(line)/2)
        half01 = Set(collect(line[1:midpoint]))
        half02 = Set(collect(line[midpoint+1:end]))
        error_type = pop!(intersect(half01, half02))
        score += get_score(error_type)
    end
    return score
end

star01()

function star02()
    for i = 1:3:length(lines)
        common = intersect(Set(collect(lines[i])), Set(collect(lines[i+1])))
        common = intersect(common, Set(collect(lines[i+2])))
        println("$common")
        break
    end


end

star02()