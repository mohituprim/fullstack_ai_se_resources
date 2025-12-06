# Introduction to Agentic AI

## What is an Agentic AI Workflow?

An agentic AI workflow is a process where an LLM-based app executes multiple steps to complete a task.

**Task Decomposition** - Task is decomposed into multiple steps.

## Degree of Autonomy

- **Low**: The agent is guided by a set of rules and instructions.
  - All steps are pre-defined and executed in sequence.
  - All tools are hardcoded and cannot be changed.
  - Autonomy is in text generation only.

- **Medium**: The agent is guided by a set of rules and instructions, but can also make decisions based on the context.
  - Agent can make some decisions based on the context, choose tools, etc.
  - Autonomy is in text generation and tool selection.
  - All tools are hardcoded and cannot be changed.

- **High**: The agent is autonomous and can make decisions based on the context.
  - Agent can make decisions based on the context, choose tools, etc.
  - Agent makes multiple decisions based on the context, choose tools, etc.
  - Can create new steps and tools based on the context.

## Degree of Intelligence

- **Low**: The agent is a rule-based agent.
- **Medium**: The agent is a hybrid agent.
- **High**: The agent is a generative agent.

## Benefits of Agentic AI Workflows

- Much better performance than traditional workflows.
- Faster than human because of parallel execution.
- Modular and reusable - Can add or update tools, swap out models.

## Evaluation of Agentic AI (Eval)

- Can evaluate using code (Objective evaluation), or LLM as judge (Subjective evaluation).
- Two types of eval: End to End, Component level.
- Examine traces to perform error analysis and debugging.

## Agentic Design Patterns

### Reflection

Reflection is a common design pattern where you can ask the LLM to examine its own outputs. Maybe bring in some external sources of information, such as run the code and see if it generates any error messages, and use that as feedback to iterate again and come up with a better version of its output.

#### Zero Shot Prompting

- 0 example prompting - Just give the LLM a task and let it figure out how to complete it.

#### One Shot Prompting

- 1 example prompting - Give the LLM a task and an example of how to complete it.

#### Few Shot Prompting

- Few examples prompting - Give the LLM a task and a few examples of how to complete it.
- This is a common design pattern where you can give the LLM a task and a few examples of how to complete it.

### Tool Use

- LLMs can be given tools, meaning functions that they can call in order to get work done.
- For example, if you ask an LLM, what's the best coffee maker according to reviewers, and you give it a web search tool, then it can actually search the internet to find much better answers.

### Planning

- This is an example from a paper called Hugging GPT, in which if you ask a system to please generate an image where a girl is reading a book and a pose is the same as a boy in the image, then please describe the new image in your voice.
- Then a model can automatically decide that to carry out this task, it first needs to find a pose determination model to figure out the pose of the boy. Then to pose the image, to generate a picture of a girl and image the text, and then finally text the speech.
- And so in planning, an LLM decides what is the sequence of actions it needs to take. In this case, it is a sequence of API calls so that it can then carry out the right sequence of steps in the right order in order to carry out the task. So rather than the developer hard coding the sequence of steps in advance, this actually lets the LLM decide what are the steps to take. Agents that plan today are harder to control and somewhat more experimental, but sometimes they can give really delightful results.

### Multi-Agent Collaboration

- Just as a human manager might hire a number of others to work together on a complex project, in some cases it might make sense for you to hire a set of multiple agents, maybe each of which specializes in a different role, and have them work together to accomplish a complex task.
