from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
from SearchAPI import *
from nltk.corpus import wordnet as wn


nltk.download('wordnet')
nltk.download('omw-1.4')

global fig_agg

# Draws the histogram onto the Canvas
def draw_figure_on_canvas(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# Deletes the histogram to replace it with a new one
def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')

# This function updates the textbox with the WordNet such as definitions and synonyms
def func(window, num, top):
    string = ""
    string = string + "Word: " + top[num] + '\n'
    term = wn.synsets(top[num])[0]  # Takes the first synset from WordNet
    window['Query'].update(str(values['Query']) + " " + top[num])   # Add the selected term into the query textbox
    list = [str(lemma.name()) for lemma in wn.synset(term.name()).lemmas()] # Find the synonyms from the first synset

    string = string + "Definition: " + term.definition() + '\n' + "Other Words: " + "\n"    # Updates the textbox with definitions and words
    for x in range(len(list)):  # Replaces the underscore from synonyms with spaces
        w = list[x].replace('_', " ")
        string = string + w + " - "
    window['WordNet'].update(string)


def refine(query, window):
    global fig_agg
    list = query.split(" ")
    wordnet_list = []
    string = ''
    for x in list:
        term = wn.synsets(x)[0] # For each split word in the query, it finds the synset and converts them into words
        wordnet_list += [str(lemma.name()) for lemma in wn.synset(term.name()).lemmas()]
    for x in range(len(wordnet_list)):  # Add the words from Wordnet into a string for the search function
        string += str(wordnet_list[x]) + " "
    string = string.replace('_', ' ')
    window['Textbox'].update(search(string))    # Uses Google API search
    if fig_agg is not None: # Update the histogram with new results
        delete_fig_agg(fig_agg)
    fig_agg = draw_figure_on_canvas(window['Canvas'].TKCanvas, plot())


left_column = [     # Left side of the GUI
    [sg.Text('Web Search')],
    [sg.Text('Enter Query: '), sg.InputText(key='Query'), sg.Button('Search', bind_return_key=True),
     sg.Button('Reset'), sg.Button('Refine', visible=False)],
    [sg.Multiline(key='Textbox', size=(80, 40), disabled=True, visible=False)]
]

middle_column = [   # Middle containing the buttons for the histogram
    [sg.Button(' 1st ', visible=False, key='b0', size=(10, 1))],
    [sg.Button(' 2nd ', visible=False, key='b1', size=(10, 1))],
    [sg.Button(' 3rd ', visible=False, key='b2', size=(10, 1))],
    [sg.Button(' 4th ', visible=False, key='b3', size=(10, 1))],
    [sg.Button(' 5th ', visible=False, key='b4', size=(10, 1))],
    [sg.Button(' 6th ', visible=False, key='b5', size=(10, 1))],
    [sg.Button(' 7th ', visible=False, key='b6', size=(10, 1))],
    [sg.Button(' 8th ', visible=False, key='b7', size=(10, 1))],
    [sg.Button(' 9th ', visible=False, key='b8', size=(10, 1))],
    [sg.Button('10th ', visible=False, key='b9', size=(10, 1))],
    [sg.Text('')],
    [sg.Text('')],
    [sg.Text('')],
    [sg.Text('')],
]

right_column = [    # Right side of GUI containing the histogram and text box
    [sg.Text('Term Frequency Histogram', visible=False, key='Histogram_Text')],
    [sg.Canvas(size=(80, 40), key='Canvas')],
    [sg.Text('WordNet', visible=False, key='WordNet_Text')],
    [sg.Multiline(key='WordNet', size=(80, 5), disabled=True, visible=False)],
]

layout = [  # The whole layout of the GUI
    [sg.Column(left_column),
     sg.VSeperator(pad=(0, 0)),
     sg.Column(middle_column),
     sg.VSeperator(pad=(0, 0)),
     sg.Column(right_column), ]
]

# Create the Window
window = sg.Window('Project', layout)
# Event Loop to process "events" and get the "values" of the inputs
fig_agg = None
while True:
    global top_results
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # If user closes window or clicks cancel
        break
    if event == 'Reset':    # If user clicks the reset query button
        window['Query'].update('')
    if event == 'Search' and values['Query'] != "" and not values['Query'].isspace(): # If user tries to click search with an empty query
        window['Textbox'].update(search(values['Query']), visible=True)
        window['Histogram_Text'].update(visible=True)
        window['Refine'].update(visible=True)
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig_agg = draw_figure_on_canvas(window['Canvas'].TKCanvas, plot())  # Draws the histogram to the canvas
        top = returnTopResult()

        for x in range(0, 10, 1):   # Creates and updates the buttons for adding terms to the query
            button_name = 'b' + str(x)
            window[button_name].update(top[x], visible=True)
        window['WordNet_Text'].update(visible=True)
        window['WordNet'].update(visible=True)
        window['Histogram_Text'].update('Term Frequency Histogram\t\t\tRating: ' + str(round(returnScore(), 3)))    # Display the rating for the query
    if event == 'Refine':   # Calls the refine function
        refine(values['Query'], window)
        top = returnTopResult()

        for x in range(0, 10, 1):
            button_name = 'b' + str(x)
            window[button_name].update(top[x], visible=True)
        window['Histogram_Text'].update('Term Frequency Histogram\t\t\tRating: ' + str(round(returnScore(), 3)))
    if event == 'b0':   # First term button
        func(window, 0, top)
    if event == 'b1':   # Second button
        func(window, 1, top)
    if event == 'b2':   # Third button
        func(window, 2, top)
    if event == 'b3':   # Fourth term button
        func(window, 3, top)
    if event == 'b4':   # Fifth term button
        func(window, 4, top)
    if event == 'b5':   # Sixth term button
        func(window, 5, top)
    if event == 'b6':   # Seventh term button
        func(window, 6, top)
    if event == 'b7':   # Eight term button
        func(window, 7, top)
    if event == 'b8':   # Ninth term button
        func(window, 8, top)
    if event == 'b9':   # Tenth term button
        func(window, 9, top)

window.close()
