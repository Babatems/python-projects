"""
Assignment 1 - Problem 2
NetLogo Version: 6.2.0
Python Version: 3.12.1
Author: Inumoh
"""

import sys
import pynetlogo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("All imports successful!")


netlogo_path = r'C:\Program Files\NetLogo 6.2.0'

if os.path.exists(netlogo_path):
    print(f"NetLogo found at: {netlogo_path}")
else:
    print("NetLogo not found!")


print("Connecting to NetLogo...")
netlogo = pynetlogo.NetLogoLink(gui=False, netlogo_home=netlogo_path)

print("NetLogo connected!")


model_path = netlogo_path + r'\app\models\Sample Models\Biology\Wolf Sheep Predation.nlogo'

if os.path.exists(model_path):
    print(f"Model found at: {model_path}")
    netlogo.load_model(model_path)
    print("Model loaded successfully!")
else:
    print("Model not found, searching...")
    import glob
    models = glob.glob(netlogo_path + r'\**\Wolf Sheep Predation.nlogo', recursive=True)
    if models:
        print(f"Found model at: {models[0]}")
        netlogo.load_model(models[0])
        print("Model loaded successfully!")

netlogo.command('setup')
print(f"\nInitial state:")
print(f"  Sheep: {netlogo.report('count sheep')}")
print(f"  Wolves: {netlogo.report('count wolves')}")


x = netlogo.report('map [s -> [xcor] of s] sort sheep')
y = netlogo.report('map [s -> [ycor] of s] sort sheep')

fig, ax = plt.subplots(1)
ax.scatter(x, y, s=4)
ax.set_xlabel('xcor')
ax.set_ylabel('ycor')
ax.set_title('Initial Sheep Positions - Inumoh')
ax.set_aspect('equal')
fig.set_size_inches(5, 5)

plt.savefig('01_initial_positions_Inumoh.png', dpi=300, bbox_inches='tight')
plt.show()

print("Initial positions plotted - Inumoh")


netlogo.command('repeat 100 [go]')

x = netlogo.report('map [s -> [xcor] of s] sort sheep')
y = netlogo.report('map [s -> [ycor] of s] sort sheep')
energy_sheep = netlogo.report('map [s -> [energy] of s] sort sheep')
energy_wolves = netlogo.report('[energy] of wolves')

print(f"After 100 ticks - Inumoh:")
print(f"  Sheep count: {len(energy_sheep)}")
print(f"  Wolf count: {len(energy_wolves)}")


from mpl_toolkits.axes_grid1 import make_axes_locatable

fig, ax = plt.subplots(1, 2)

sc = ax[0].scatter(x, y, s=50, c=energy_sheep, cmap=plt.cm.coolwarm)
ax[0].set_xlabel('xcor')
ax[0].set_ylabel('ycor')
ax[0].set_title('Sheep Positions After 100 Ticks - Inumoh')
ax[0].set_aspect('equal')
divider = make_axes_locatable(ax[0])
cax = divider.append_axes('right', size='5%', pad=0.1)
cbar = plt.colorbar(sc, cax=cax, orientation='vertical')
cbar.set_label('Energy of sheep')

sns.histplot(energy_sheep, kde=False, bins=10, ax=ax[1], label='Sheep', alpha=0.7)
sns.histplot(energy_wolves, kde=False, bins=10, ax=ax[1], label='Wolves', alpha=0.7)
ax[1].set_xlabel('Energy')
ax[1].set_ylabel('Counts')
ax[1].set_title('Energy Distribution - Inumoh')
ax[1].legend()

fig.set_size_inches(14, 5)
plt.tight_layout()
plt.savefig('02_energy_distribution_Inumoh.png', dpi=300, bbox_inches='tight')
plt.show()

print("Energy distribution plotted - Inumoh")


netlogo.command('setup')
counts_data = netlogo.repeat_report(['count wolves', 'count sheep'], 200, go='go')


counts = pd.DataFrame(counts_data)

print("\nPopulation Data - Inumoh")
print(counts.head(10))
print("\n...")
print(counts.tail(10))


fig, (ax1, ax2) = plt.subplots(1, 2)

counts.plot(ax=ax1, use_index=True, legend=True)
ax1.set_xlabel('Ticks')
ax1.set_ylabel('Counts')
ax1.set_title('Population Over Time - Inumoh')
ax1.grid(True, alpha=0.3)

ax2.plot(counts['count wolves'], counts['count sheep'])
ax2.set_xlabel('Wolves')
ax2.set_ylabel('Sheep')
ax2.set_title('Phase Space Plot - Inumoh')
ax2.grid(True, alpha=0.3)

fig.set_size_inches(12, 5)
plt.tight_layout()
plt.savefig('03_population_dynamics_Inumoh.png', dpi=300, bbox_inches='tight')
plt.show()

print("Population dynamics plotted - Inumoh")


energy_data = netlogo.repeat_report(['[energy] of wolves',
                                   '[energy] of sheep',
                                   'count sheep',
                                   'count wolves'], 5)

energy_df = pd.DataFrame(energy_data)

print("\nEnergy Data Sample - Inumoh")
print(energy_df.head())

fig, ax = plt.subplots(1)
sns.histplot(energy_df['[energy] of wolves'].iloc[-1], kde=False, bins=20, ax=ax)
ax.set_xlabel('Energy')
ax.set_ylabel('Counts')
ax.set_title('Wolf Energy Distribution (Final Tick) - Inumoh')
fig.set_size_inches(6, 4)
plt.savefig('04_wolf_energy_Inumoh.png', dpi=300, bbox_inches='tight')
plt.show()

print("Wolf energy plotted - Inumoh")


countdown_df = netlogo.patch_report('countdown')

print("\nPatch Countdown Data - Inumoh")
print(f"Shape: {countdown_df.shape}")
print(countdown_df.head())

fig, ax = plt.subplots(1)
patches = sns.heatmap(countdown_df, xticklabels=5, yticklabels=5,
                      cbar_kws={'label':'countdown'}, ax=ax)
ax.set_xlabel('pxcor')
ax.set_ylabel('pycor')
ax.set_title('Grass Countdown Heatmap - Inumoh')
ax.set_aspect('equal')
fig.set_size_inches(8, 6)
plt.tight_layout()
plt.savefig('05_heatmap_Inumoh.png', dpi=300, bbox_inches='tight')
plt.show()

print("Heatmap plotted - Inumoh")


print("\n" + "="*70)
print("SUMMARY STATISTICS - INUMOH")
print("="*70)
print("\nPopulation Statistics:")
print(counts.describe())

print("\n" + "="*70)
print("Final State - Inumoh:")
print(f"  Final Wolves: {counts['count wolves'].iloc[-1]}")
print(f"  Final Sheep: {counts['count sheep'].iloc[-1]}")
print(f"  Mean Wolves: {counts['count wolves'].mean():.2f}")
print(f"  Mean Sheep: {counts['count sheep'].mean():.2f}")
print("="*70)

netlogo.kill_workspace()