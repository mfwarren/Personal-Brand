# How a Holiday Tech Support Call Turned Into a Full-Stack AI Project

Like many eldest sons, I have a standing role as family tech support. This holiday season, that role led me somewhere unexpected: launching a new product.

## The Call

I was visiting my parents over the holidays when they asked for help with a recipe app called MasterCook. They'd been using it for years, but the service was being decommissioned. Could I help them migrate their recipes somewhere else?

I looked at the recommended migration path. Then I looked at the replacement applications. They were... not great. Clunky interfaces, limited features, the kind of software that feels abandoned even when it's technically still maintained.

I had a week of vacation left. I thought: I can build something better than this.

## One Week Later

That thought became [save.cooking](https://save.cooking) - and it's grown far beyond what I originally imagined.

What started as a simple tool to import MasterCook recipe files has evolved into a fully-featured AI-enhanced meal planning platform:

**Core Features:**
- Import recipes from MasterCook (.mxp, .mx2) and other formats
- AI-powered recipe parsing that actually understands ingredients and instructions
- Vector embeddings that map recipe similarity - find dishes related to ones you love
- Automatic shopping list generation synced to your weekly meal plan
- Public recipe sharing with user profiles
- Full meal plan sharing - not just individual recipes

**Technical Details I Never Would Have Tackled Alone:**
- JSON-LD structured data for Google Recipe rich results
- Pinterest-optimized images and metadata
- Open Graph tags specifically tuned for recipe content
- Responsive Next.js frontend (not my usual stack)

The site already has over 300 public recipes in its database, and that number grows daily.

## The AI Difference

Here's the thing: I'm not a Next.js developer. I've built backends, APIs, CLIs - but modern React frontends aren't my wheelhouse. A year ago, this project would have taken months and looked significantly worse.

With Claude Code handling the heavy lifting, I could focus on product decisions while the AI handled implementation details. Need Pinterest meta tags? Claude knew the exact format. Want vector similarity search? Claude set up the embeddings pipeline. Struggling with a responsive layout? Claude fixed the CSS.

This isn't about AI writing code for me. It's about AI expanding what I can realistically build. The cognitive load of learning a new framework while also designing features while also handling deployment - that's usually where side projects die. AI agents absorbed that load.

## The Graveyard Problem

Recipe websites are a graveyard. AllRecipes feels like it hasn't been updated since 2010. Food blogs are drowning in ads and life stories before you get to the actual recipe. Apps come and go, taking your data with them.

People have stopped expecting good software in this space. They've accepted that finding a recipe means scrolling past someone's childhood memories and closing seventeen popups.

I think we can do better. I think we should do better. Cooking is fundamental - it's one of the few things that genuinely brings people together. The software around it shouldn't be an obstacle.

## What's Next

save.cooking is live and growing. I'm using it daily for my own meal planning. Features are shipping weekly:

- Ingredient substitution suggestions
- Nutritional analysis
- Collaborative meal planning for households
- Recipe scaling that actually works
- Smarter shopping list organization by store section

If you've got recipes trapped in old software, or you're just tired of the current options, come check it out at [save.cooking](https://save.cooking).

And if you're a developer wondering what you could build in a week with AI assistance - the answer might surprise you. The constraint isn't technical capability anymore. It's just deciding what's worth building.

---

*Built with Claude Code over a holiday week. The family tech support call that actually paid off.*
