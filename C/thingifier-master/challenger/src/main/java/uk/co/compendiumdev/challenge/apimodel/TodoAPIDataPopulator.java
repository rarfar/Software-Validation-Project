package uk.co.compendiumdev.challenge.apimodel;

import uk.co.compendiumdev.thingifier.core.EntityRelModel;
import uk.co.compendiumdev.thingifier.core.domain.definitions.ERSchema;
import uk.co.compendiumdev.thingifier.core.domain.instances.ERInstanceData;
import uk.co.compendiumdev.thingifier.core.domain.instances.EntityInstance;
import uk.co.compendiumdev.thingifier.core.domain.instances.EntityInstanceCollection;
import uk.co.compendiumdev.thingifier.core.domain.datapopulator.DataPopulator;

public class TodoAPIDataPopulator implements DataPopulator {

    @Override
    public void populate(final ERSchema schema, final ERInstanceData database) {

        String [] todos={
                        "scan paperwork",
                        "file paperwork",
                        "process payments",
                        "escalate late payments",
                        "pay invoices",
                        "process payroll",
                        "train staff",
                        "schedule meeting",
                        "tidy meeting room",
                        "install webcam"};

        EntityInstanceCollection todo = database.getInstanceCollectionForEntityNamed("todo");

        for(String todoItem : todos){
            EntityInstance instance = new EntityInstance(todo.definition());
            todo.addInstance(instance);
            instance.setValue("title", todoItem);
        }
    }
}
