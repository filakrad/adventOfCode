using DataStructures

loaded = read("./day11.txt", String)
inputs = split(loaded, "\n\n")

int = v -> parse(Int128, v)

mutable struct Monkey 
    id::Int
    items::Deque{Int128}
    operation::Function
    divisible::Int
    if_true::Int
    if_false::Int
    inspected::Int
end

function fill_monkeys(monkeys)
    for inp in inputs
        lines = split(inp, "\n")
        id = match(r"Monkey (\d+):", lines[1]) |> m -> int(m[1]) + 1
        items = split(replace(lines[2], r"Starting items: "=>""), ",") .|> int
        operation = replace(lines[3], r"Operation: new = "=>"")
        operation = "old -> " * operation
        op = eval(Meta.parse(operation))
        divisible = match(r"Test: divisible by (\d+)", lines[4])  |> m -> int(m[1])
        if_true = match(r"If true: throw to monkey (\d+)", lines[5])  |> m -> int(m[1]) + 1
        if_false = match(r"If false: throw to monkey (\d+)", lines[6])  |> m -> int(m[1]) + 1
        push!(monkeys, Monkey(id, Deque{Int128}(), op, divisible, if_true, if_false, 0))
        for item in items
            push!(monkeys[id].items, item)
        end
    end
end

function throw_item_01(monkey, monkeys)
    monkey.inspected += 1
    item = popfirst!(monkey.items)
    item = Base.invokelatest(monkey.operation, item)
    item = item ÷ 3
    if mod(item, monkey.divisible) == 0
        push!(monkeys[monkey.if_true].items, item)
    else
        push!(monkeys[monkey.if_false].items, item)
    end
end

function do_turn_01(monkey, monkeys)
    while ! isempty(monkey.items)
        throw_item_01(monkey, monkeys)
    end
end

function do_round_01(monkeys)
    for monkey in monkeys
        do_turn_01(monkey, monkeys)
    end
end

function part01()
    monkeys = []
    fill_monkeys(monkeys)
    for _ in 1:20
        do_round_01(monkeys)
    end
    insp = [m.inspected for  m in monkeys]
    sort!(insp, rev=true)
    return insp[1]*insp[2]
end

function throw_item_02(monkey, monkeys, big_modulo)
    monkey.inspected += 1
    item = popfirst!(monkey.items)
    item = Base.invokelatest(monkey.operation, item)
    item = item % big_modulo
    if mod(item, monkey.divisible) == 0
        push!(monkeys[monkey.if_true].items, item)
    else
        push!(monkeys[monkey.if_false].items, item)
    end
end

function do_turn_02(monkey, monkeys, big_modulo)
    while ! isempty(monkey.items)
        throw_item_02(monkey, monkeys, big_modulo)
    end
end

function do_round_02(monkeys, big_modulo)
    for monkey in monkeys
        do_turn_02(monkey, monkeys, big_modulo)
    end
end

function part02()
    monkeys = []
    fill_monkeys(monkeys)
    big_modulo = prod(m.divisible for m in monkeys)
    for _ in 1:10000
        do_round_02(monkeys, big_modulo)
    end
    insp = [m.inspected for  m in monkeys]

    sort!(insp, rev=true)
    return insp[1]*insp[2]
end

println(part01())
println(part02())

