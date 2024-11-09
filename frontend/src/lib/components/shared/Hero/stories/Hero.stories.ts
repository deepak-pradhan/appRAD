
// src/stories/Hero.stories.ts
import type { Meta, StoryObj } from '@storybook/svelte';
import Hero from '../Hero.svelte';

const meta = {
  title: 'Components/Hero',  // Defines location in Storybook's sidebar
  component: Hero,           // Links to our Hero.svelte component
  tags: ['autodocs']        // Enables automatic documentation
} satisfies Meta<Hero>;

export default meta;
type Story = StoryObj<typeof meta>;

// src/stories/Hero.stories.ts
export const Primary: Story = {
  args: {
    title: 'Build Powerful Apps',
    subtitle: 'Visual Development Platform',
    ctaText: 'Get Started'
  }
};

export const WithHighlight: Story = {
  args: {
    title: 'Build Powerful Apps with LLM',
    subtitle: 'AI-Powered Visual Development',
    ctaText: 'Start Building'
  }
};
