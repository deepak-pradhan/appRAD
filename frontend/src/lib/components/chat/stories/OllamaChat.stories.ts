
// lib/components/chat/stories/OllamaChat.stories.ts
import type { Meta, StoryObj } from '@storybook/svelte';
import OllamaChat from '../OllamaChat.svelte';

const meta = {
  title: 'Chat/OllamaChat',
  component: OllamaChat,
  tags: ['autodocs']
} satisfies Meta<OllamaChat>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    modelName: 'llama2',
    theme: 'dark'
  }
};
