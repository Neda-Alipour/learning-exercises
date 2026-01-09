import React from "react";
import Card from "./Card";
import emojipedia from "./../emojipedia.js";

function createCard(item) {
  return (
    <Card
      key={item.id}
      emoji={item.emoji}
      name={item.name}
      meaning={item.meaning}
    />
  );
}

function App() {
  return (
    <div>
      <h1>
        <span>emojipedia</span>
      </h1>
      <div>
        <dl className="dictionary">{emojipedia.map(createCard)}</dl>
      </div>
    </div>
  );
}

export default App;
