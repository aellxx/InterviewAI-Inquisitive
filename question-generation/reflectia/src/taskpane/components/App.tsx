import * as React from 'react';

import Progress from './progress';

export interface AppProps {
    title: string;
    isOfficeInitialized: boolean;
}

export default function App({ title, isOfficeInitialized }: AppProps) {
    async () => {
        return Word.run(async (context) => {
            /**
             * Insert your Word code here
             */

            // insert a paragraph at the end of the document.
            const paragraph = context.document.body.insertParagraph(
                'Hello World',
                Word.InsertLocation.end
            );

            // change the paragraph color to blue.
            paragraph.font.color = 'blue';

            await context.sync();
        });
    };

    if (!isOfficeInitialized)
        return (
            <Progress
                title={title}
                logo={require('./../../../assets/logo-filled.png')}
                message="Please sideload your addin to see app body."
            />
        );

    return <div className="ms-welcome"></div>;
}
