using DelimitedFiles

z = DelimitedFiles.readdlm("pokus2021-01.txt", '\n', Int)

function get_increases(z)
    bools = [x < y for (x, y) in zip(z, z[2:end])]
    return sum(bools)
end

println(get_increases(z))

x = [sum(t) for t in zip(z, z[2:end], z[3:end])]
print(get_increases(x))