// src/stories/Features.stories.ts
import type { Meta, StoryObj } from '@storybook/svelte';
import Features from '../Features.svelte';

const meta = {
  title: 'Components/Features',
  component: Features,
  tags: ['autodocs']
} satisfies Meta<Features>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    features: [
      {
        title: 'LLM Integration',
        description: 'Powerful language model capabilities'
      },
      {
        title: 'Visual Flows',
        description: 'Build workflows with Rete.js'
      },
      {
        title: 'Database Management',
        description: 'Intuitive data handling with Partyql'
      },
      {
        title: 'Code Generation',
        description: 'Automated development tools'
      }
    ]
  }
};
