import csv

team_0_data = """
Natus Vincere Natus Vincere	K (hs)	A (f)	D	KAST	K-D Diff	ADR	FK Diff	Rating 2.1
Romania iM	18 (10)	7 (0)	15	75.0%	+3	88.1	0	1.37
Ukraine w0nderful	24 (12)	8 (3)	17	79.2%	+7	98.6	0	1.36
Lithuania jL	20 (10)	6 (0)	15	83.3%	+5	93.2	-3	1.25
Ukraine b1t	20 (11)	3 (0)	16	83.3%	+4	84.1	+3	1.24
Finland Aleksib	9 (4)	8 (4)	14	75.0%	-5	45.5	0	0.78
"""

team_1_data = """
MOUZ MOUZ	K (hs)	A (f)	D	KAST	K-D Diff	ADR	FK Diff	Rating 2.1
Finland Jimpphat	21 (10)	7 (2)	18	70.8%	+3	77.2	+1	1.19
Sweden Brollan	19 (11)	2 (0)	16	75.0%	+3	67.3	0	1.10
Israel xertioN	16 (9)	10 (1)	22	66.7%	-6	94.9	-2	1.00
Hungary torzsi	13 (2)	4 (1)	17	66.7%	-4	56.8	+4	0.81
Poland siuhy	8 (6)	7 (1)	20	62.5%	-12	54.7	-3	0.60
"""
team_0_ranking = 1
team_1_ranking = 5
winner = 0

# 07 Out 2024
# 1 - NaVi          # 11 - SAW
# 2 - G2            # 12 - paiN
# 3 - Vitality      # 13 - The MongolZ
# 4 - Spirit        # 14 - FURIA
# 5 - MOUZ          # 15 - MIBR
# 6 - FaZe          # 16 - HEROIC
# 7 - Eternal Fire  # 17 - Astralis
# 8 - Liquid        # 19 - M80
# 9 - VP            # 18 - Falcons
# 10 - Complexity   # 20 - BIG

# 23 Sep 2024
# 1 - NaVi          # 11 - VP
# 2 - Vitality      # 13 - paiN
# 3 - G2            # 12 - The MongolZ
# 4 - Spirit        # 15 - MIBR
# 5 - MOUZ          # 14 - SAW
# 6 - Eternal Fire  # 17 - Astralis
# 7 - FaZe          # 16 - MIBR
# 8 - Liquid        # 19 - Falcons
# 9 - Complexity    # 18 - FURIA
# 10 - SAW          # 20 - Astralis

# 28 Out 2024
# 1 - NaVi          # 11 - FURIA
# 2 - G2            # 12 - Complexity
# 3 - Vitality      # 13 - The MongolZ
# 4 - MOUZ          # 14 - SAW
# 5 - Spirit        # 15 - paiN
# 6 - FaZe          # 16 - MIBR
# 7 - Eternal Fire  # 17 - Astralis
# 8 - HEROIC        # 18 - BIG
# 9 - Liquid        # 19 - M80
# 10 - VP           # 20 - Sangal

# 10 Fev 2025
# 1 - Spirit        # 11 - Astralis
# 2 - Vitality      # 12 - FURIA
# 3 - NaVi          # 13 - GL
# 4 - G2            # 14 - Falcons
# 5 - Eternal Fire  # 15 - paiN
# 6 - FaZe          # 16 - 3DMAX
# 7 - The MongolZ   # 17 - MIBR
# 8 - MOUZ          # 18 - BIG
# 9 - Liquid        # 19 - BetBoom
# 10 - VP           # 20 - HEROIC

# Team 0 | Team 0 HLTV Ranking | Team 0 Average HLTV 2.1 Rating | Team 0 Total Kills | Team 0 Total Assists | Team 0 Total Deaths | Team 0 Average Kills | Team 0 Average Assists | Team 0 Average Deaths | Team 0 Average ADR
# Team 1 | Team 1 HLTV Ranking | Team 1 Average HLTV 2.1 Rating | Team 1 Total Kills | Team 1 Total Assists | Team 1 Total Deaths | Team 1 Average Kills | Team 1 Average Assists | Team 1 Average Deaths | Team 1 Average ADR
# | Delta HLTV Ranking | Delta HLTV Rating | Delta Kills | Delta Assists | Delta Deaths | Delta ADR | Winner

team_0_lines = team_0_data.strip().split('\n')
team_1_lines = team_1_data.strip().split('\n')

team_0_stats = []
total_rating_0 = 0
total_kills_0 = 0
total_assists_0 = 0
total_deaths_0 = 0
total_adr_0 = 0

for index, line in enumerate(team_0_lines):
  row = line.split('\t')
  if index == 0:
    team_0_stats.append(row[0])
  else:
    total_rating_0 += float(row[8])
    total_kills_0 += int(row[1].split(' ')[0])
    total_assists_0 += int(row[2].split(' ')[0])
    total_deaths_0 += int(row[3])
    total_adr_0 += float(row[6])

team_0_stats.append(str(team_0_ranking))
team_0_stats.append(f"{total_rating_0 / 5: .2f}")
team_0_stats.append(str(total_kills_0))
team_0_stats.append(str(total_assists_0))
team_0_stats.append(str(total_deaths_0))
team_0_stats.append(f"{total_kills_0 / 5: .2f}")
team_0_stats.append(f"{total_assists_0 / 5: .2f}")
team_0_stats.append(f"{total_deaths_0 / 5: .2f}")
team_0_stats.append(f"{total_adr_0 / 5: .2f}")

team_1_stats = []
total_rating_1 = 0
total_kills_1 = 0
total_assists_1 = 0
total_deaths_1 = 0
total_adr_1 = 0

for index, line in enumerate(team_1_lines):
  row = line.split('\t')
  if index == 0:
    team_1_stats.append(row[0])
  else:
    total_rating_1 += float(row[8])
    total_kills_1 += int(row[1].split(' ')[0])
    total_assists_1 += int(row[2].split(' ')[0])
    total_deaths_1 += int(row[3])
    total_adr_1 += float(row[6])

team_1_stats.append(str(team_1_ranking))
team_1_stats.append(f"{total_rating_1 / 5: .2f}")
team_1_stats.append(str(total_kills_1))
team_1_stats.append(str(total_assists_1))
team_1_stats.append(str(total_deaths_1))
team_1_stats.append(f"{total_kills_1 / 5: .2f}")
team_1_stats.append(f"{total_assists_1 / 5: .2f}")
team_1_stats.append(f"{total_deaths_1 / 5: .2f}")
team_1_stats.append(f"{total_adr_1 / 5: .2f}")
team_1_stats.append(str(team_0_ranking - team_1_ranking))
team_1_stats.append(f"{float(team_0_stats[2]) - float(team_1_stats[2]): .2f}")
team_1_stats.append(str(total_kills_0 - total_kills_1))
team_1_stats.append(str(total_assists_0 - total_assists_1))
team_1_stats.append(str(total_deaths_0 - total_deaths_1))
team_1_stats.append(f"{total_adr_0 - total_adr_1: .1f}")
team_1_stats.append(str(winner))

with open('Redes_Neurais/final_project/cs2_stats.csv', mode='a', newline='', encoding='utf-8') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(team_0_stats + team_1_stats)
