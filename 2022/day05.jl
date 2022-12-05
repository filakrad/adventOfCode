# import Pkg
# Pkg.add("DataStructures")

using DataStructures

loaded = read("./day05.txt", String)
stacks_input, moves_input = split(loaded, "\n\n")

int = v -> parse(Int, v)

function get_stacks()
    stack_input_rows = split(stacks_input, "\n")
    pop!(stack_input_rows)
    lng = length(stack_input_rows[1]) ÷ 4 + 1
    stacks = [Stack{Char}() for _ in 1:lng]
    for row in reverse(stack_input_rows)
        for (ri, si) in enumerate(2:4:length(stack_input_rows[1]))
            if row[si] != ' '
                push!(stacks[ri], row[si])
            end
        end
    end
    return stacks
end

function get_moves()
    moves_input_rows = split(moves_input, "\n")
    moves = []
    for row in moves_input_rows
        x = match(r"move (\d+) from (\d+) to (\d+)", row) |> m -> (int(m[1]), int(m[2]), int(m[3]))
        push!(moves, x)
    end
    return moves
end


function part01()
    stacks = get_stacks()
    moves = get_moves()
    for move in moves
        for _ in 1:move[1]
            tmp = pop!(stacks[move[2]])
            push!(stacks[move[3]], tmp)
        end
    end
    result = ""
    for stack in stacks
        result *= pop!(stack)
    end
    return result
end

function part02()
    stacks = get_stacks()
    moves = get_moves()
    for move in moves
        tmp_stack = Stack{Char}()
        for _ in 1:move[1]
            tmp = pop!(stacks[move[2]])
            push!(tmp_stack, tmp)
        end
        while ! isempty(tmp_stack)
            push!(stacks[move[3]], pop!(tmp_stack))
        end
    end
    result = ""
    for stack in stacks
        result *= pop!(stack)
    end
    return result
end


println(part01())
println(part02())


