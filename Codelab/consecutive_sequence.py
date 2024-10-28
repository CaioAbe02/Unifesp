# Find the largest consecutive sequence

def findSequence(nums):
    # transforma o array em um set, já que as buscas em um set é O(1) e O(n) para um list
    nums_set = set(nums)
    longest_seq = 1

    for num in nums_set:
        # verifica se há o número anterior para que o while só rode no número inicial de cada sequência
        if num - 1 not in nums_set:
            current_num = num
            current_seq = 1

            # roda enquanto há números consecutivos no array
            while current_num + 1 in nums_set:
                current_seq += 1
                current_num += 1

            # verifica se a atual sequência é a maior
            if current_seq > longest_seq:
                longest_seq = current_seq

    return longest_seq

nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
print(findSequence(nums))
