
import graphviz
from collections import deque

class NFAEngine:
    def __init__(self):
        self.state_counter = 0

    def get_state(self):
        self.state_counter += 1
        return self.state_counter

    def preprocess_regex(self, regex):
        """Insert explicit concatenation operators (.)"""
        if not regex:
            return ""
        
        # Clean up: remove spaces
        regex = regex.replace(" ", "")
        
        result = ""
        for i, char in enumerate(regex):
            result += char
            if i + 1 < len(regex):
                next_char = regex[i + 1]
                # Insert . between:
                # 1. Literal and Literal (a b)
                # 2. Literal and ( (a (b))
                # 3. * and Literal (* a)
                # 4. * and ( (* ()
                # 5. ) and Literal () a)
                # 6. ) and ( () () )
                is_curr_literal = char.isalnum() or char in ['*', ')']
                is_next_literal = next_char.isalnum() or next_char == '('
                
                # Special handling: Don't insert after ( or |
                if char in ['(', '|', '+']:
                    continue
                
                if (char.isalnum() or char == ')' or char == '*') and \
                   (next_char.isalnum() or next_char == '('):
                     result += '.'
        
        # Handle + as | for convenience
        return result.replace('+', '|')

    def shunting_yard(self, regex):
        """Convert regex to postfix notation"""
        output = []
        operators = []
        precedence = {'*': 3, '.': 2, '|': 1}
        
        for char in regex:
            if char.isalnum():
                output.append(char)
            elif char == '(':
                operators.append(char)
            elif char == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop() # Pop (
            elif char in precedence:
                while (operators and operators[-1] != '(' and 
                       precedence.get(operators[-1], 0) >= precedence[char]):
                    output.append(operators.pop())
                operators.append(char)
        
        while operators:
            output.append(operators.pop())
        
        return "".join(output)

    def generate_nfa(self, regex):
        """Build NFA from regex using Thompson's Construction"""
        self.state_counter = 0
        postfix = self.shunting_yard(self.preprocess_regex(regex))
        stack = []
        
        # Edge list: (from, to, label)
        edges = []
        # Keep track of all created edges to visualize later
        
        for char in postfix:
            if char.isalnum(): # Literal
                start = self.get_state()
                end = self.get_state()
                edges.append({'from': start, 'to': end, 'label': char})
                stack.append({'start': start, 'end': end, 'edges': edges})
                # Note: 'edges' here is reference to the main list, 
                # but we actually just need to track structure.
                # Simplified: The stack items will just allow us to find start/end states.
                # The 'edges' list grows globally for this NFA.
            
            elif char == '.': # Concatenation
                right = stack.pop()
                left = stack.pop()
                # Join left.end -> right.start with epsilon
                edges.append({'from': left['end'], 'to': right['start'], 'label': 'ε'})
                stack.append({'start': left['start'], 'end': right['end']})
            
            elif char == '|': # Union
                right = stack.pop()
                left = stack.pop()
                start = self.get_state()
                end = self.get_state()
                
                # Split from new start
                edges.append({'from': start, 'to': left['start'], 'label': 'ε'})
                edges.append({'from': start, 'to': right['start'], 'label': 'ε'})
                
                # Merge to new end
                edges.append({'from': left['end'], 'to': end, 'label': 'ε'})
                edges.append({'from': right['end'], 'to': end, 'label': 'ε'})
                
                stack.append({'start': start, 'end': end})
            
            elif char == '*': # Kleene Star
                target = stack.pop()
                start = self.get_state()
                end = self.get_state()
                
                edges.append({'from': start, 'to': target['start'], 'label': 'ε'}) # Enter
                edges.append({'from': start, 'to': end, 'label': 'ε'})             # Skip
                edges.append({'from': target['end'], 'to': target['start'], 'label': 'ε'}) # Loop
                edges.append({'from': target['end'], 'to': end, 'label': 'ε'})     # Exit
                
                stack.append({'start': start, 'end': end})

        if not stack:
            return None

        final_nfa = stack.pop()
        final_nfa['edges'] = edges # Include all edges accumulated
        return final_nfa

    def get_dot(self, regex):
        try:
            nfa = self.generate_nfa(regex)
            if not nfa:
                return None
            
            dot = 'digraph {\n'
            dot += '    rankdir=LR;\n'
            dot += '    bgcolor="transparent";\n'
            dot += '    edge [color=white, fontcolor=white];\n'
            dot += '    node [shape=circle, style=filled, fillcolor="white", fontcolor="black"];\n'
            
            # Label special nodes
            dot += f'    S [label="{nfa["start"]}", shape=circle, style=filled, fillcolor="#e0f7fa"];\n'
            dot += f'    F [label="{nfa["end"]}", shape=doublecircle, style=filled, fillcolor="#ffd54f"];\n'
            
            # Start arrow
            dot += f'    StartInput [shape=point, width=0];\n'
            dot += f'    StartInput -> S;\n'

            unique_edges = set() 
            # prevent duplicates if any, though our logic is tree-like mostly
            
            for e in nfa['edges']:
                # Remap start/end to S/F for visualization if we strictly wanted simple labels,
                # but numbers are better for complex graphs.
                # Actually, let's keep numbers but color start/end.
                
                u, v = e['from'], e['to']
                # Use S/F alias in defining edges? No, names must match.
                # We defined nodes S and F above with labels. 
                # Better to just define node attributes for specific IDs.
                
                # Rewrite DOT header to be simpler
                pass

            # Let's rebuild the body properly
            # Attributes for Start/Final
            dot += f'    {nfa["start"]} [label="Start ({nfa["start"]})", style=filled, fillcolor="#b2fab4"];\n'
            dot += f'    {nfa["end"]} [label="Final ({nfa["end"]})", shape=doublecircle, style=filled, fillcolor="#ffd54f"];\n'

            for e in nfa['edges']:
                label = e['label']
                if label == 'ε':
                    label = 'ε'
                dot += f'    {e["from"]} -> {e["to"]} [label="{label}"];\n'
            
            dot += '}'
            return dot
        except Exception as e:
            return f"Error: {str(e)}"

