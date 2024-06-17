def summarize_cards(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Dictionary to count occurrences of each card
    card_counts = {}
    total_splits = 0
    ink_hits = 0
    gold_hits = 0
    krackle_hits = 0
    ink_krackle_hits = 0
    gold_krackle_hits = 0

    for line in lines:
        total_splits += 1
        card_name = line.split()[0]
        if card_name in card_counts:
            card_counts[card_name] += 1
        else:
            card_counts[card_name] = 1

        # Check for additional criteria
        if "Ink" in line:
            ink_hits += 1
        if "GoldFoil" in line:
            gold_hits += 1
        if "Kirby" in line:
            krackle_hits += 1
        if "Ink" in line and "Kirby" in line:
            ink_krackle_hits += 1
        if "GoldFoil" in line and "Kirby" in line:
            gold_krackle_hits += 1

    # Calculate Ink Rolls, Gold Rolls, and Krackle Rolls
    ink_rolls = 0
    gold_rolls = 0
    krackle_rolls = 0
    for count in card_counts.values():
        if count >= 4:
            ink_rolls += (count - 3)
        if count >= 5:
            gold_rolls += (count - 4)
        if count >= 6:
            krackle_rolls += (count - 5)

    # Write the summary to the output file
    with open(output_file, 'w') as file:
        file.write(f"Total splits: {total_splits}\n")
        file.write(f"Ink Rolls: {ink_rolls}\n")
        file.write(f"Ink Hits: {ink_hits}\n")
        file.write(f"Gold Rolls: {gold_rolls}\n")
        file.write(f"Gold Hits: {gold_hits}\n")
        file.write(f"Krackle Rolls: {krackle_rolls}\n")
        file.write(f"Krackle Hits: {krackle_hits}\n")
        file.write(f"Ink & Krackle Hits: {ink_krackle_hits}\n")
        file.write(f"Gold & Krackle Hits: {gold_krackle_hits}\n\n")

        # Sort cards by count in descending order and write to file
        for card, count in sorted(card_counts.items(), key=lambda item: item[1], reverse=True):
            file.write(f"{card} {count}\n")

# Call the function with the input and output file paths
summarize_cards('output.txt', 'summary.txt')
